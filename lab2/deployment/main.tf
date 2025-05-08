provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "microservices-cluster"
}

# === LOCAL VALUES ===
locals {
  services = {
    "booking-service"      = 8000
    "cleaning-service"     = 8001
    "dining-service"       = 8002
    "accounting-service"   = 8003
    "notification-service" = 8004
  }

  allowed_ports = [5432, 5672]
}

# === LOAD BALANCER ===
resource "aws_lb" "main" {
  name               = "microservices-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb_sg.id]
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Not Found"
      status_code  = "404"
    }
  }
}

# === SECURITY GROUPS ===
resource "aws_security_group" "alb_sg" {
  name   = "alb-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "service_sg" {
  name   = "services-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 8000
    to_port     = 8004
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Security Group for Databases
resource "aws_security_group" "db_sg" {
  name   = "lab2-db-sg"
  vpc_id = data.aws_vpc.default.id

  dynamic "ingress" {
    for_each = local.allowed_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# === IAM Role for ECS ===
data "aws_iam_role" "existing_ecs_role" {
  name = "LabRole" # or whatever name exists in your lab
}


# === ECS TASK DEFINITIONS ===
resource "aws_ecs_task_definition" "services" {
  for_each = local.services

  family                   = each.key
  requires_compatibilities = ["FARGATE"]
  network_mode            = "awsvpc"
  cpu                     = "256"
  memory                  = "512"
  execution_role_arn      = data.aws_iam_role.existing_ecs_role.arn
  task_role_arn           = data.aws_iam_role.existing_ecs_role.arn

  container_definitions = jsonencode([{
    name  = each.key
    image = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${each.key}:latest"
    portMappings = [{
      containerPort = each.value
      hostPort      = each.value
    }]
    essential = true
    environment = [
      {
        name  = "ENV"
        value = "production"
      }
    ]
  }])
}

# === ALB ROUTING ===
resource "aws_lb_target_group" "tg" {
  for_each = local.services

  name     = replace(each.key, "-", "")
  port     = each.value
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
  target_type = "ip"

  health_check {
    path     = "/"
    protocol = "HTTP"
    matcher  = "200-399"
  }
}

resource "aws_lb_listener_rule" "routing" {
  for_each = local.services

  listener_arn = aws_lb_listener.http.arn

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg[each.key].arn
  }

  condition {
    path_pattern {
      values = ["/${replace(each.key, "-service", "")}*"]
    }
  }
}

# === ECS SERVICES ===
resource "aws_ecs_service" "services" {
  for_each = local.services

  name            = each.key
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.services[each.key].arn
  launch_type     = "FARGATE"
  desired_count   = 1
  platform_version = "LATEST"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    assign_public_ip = true
    security_groups  = [aws_security_group.service_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.tg[each.key].arn
    container_name   = each.key
    container_port   = each.value
  }

  depends_on = [aws_lb_listener_rule.routing]
}

# === DATABASES ===
resource "aws_db_subnet_group" "default" {
  name       = "lab2-subnet-group"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "services" {
  for_each               = var.dbs
  identifier             = "${each.key}-instance"
  allocated_storage      = 30
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro"
  username               = var.db_user
  password               = var.db_password
  db_name                = each.value
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = true
}