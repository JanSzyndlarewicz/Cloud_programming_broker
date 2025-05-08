# Ustawienie providera AWS i regionu, z którego będą korzystać zasoby
provider "aws" {
  region = var.aws_region
}

# Pobranie danych o domyślnej VPC w danym regionie
data "aws_vpc" "default" {
  default = true
}

# Pobranie subnetów przypisanych do domyślnej VPC
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Lista dozwolonych portów do otwarcia w Security Group (np. PostgreSQL i RabbitMQ)
locals {
  allowed_ports = [5432, 5672]
}

# Utworzenie grupy bezpieczeństwa dla bazy danych
resource "aws_security_group" "db_sg" {
  name   = "lab2-db-sg"
  vpc_id = data.aws_vpc.default.id

  # Dynamiczne tworzenie reguł przychodzących (ingress) dla każdego portu z listy
  dynamic "ingress" {
    for_each = local.allowed_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]  # Zezwolenie na dostęp z dowolnego IP (można zawęzić)
    }
  }

  # Reguła wychodząca - zezwolenie na cały ruch wychodzący
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Utworzenie grupy subnetów dla instancji RDS
resource "aws_db_subnet_group" "default" {
  name       = "lab2-subnet-group"
  subnet_ids = data.aws_subnets.default.ids
}

# Tworzenie instancji bazy danych PostgreSQL dla każdej pary klucz-wartość w var.dbs
resource "aws_db_instance" "services" {
  for_each               = var.dbs  # Mapowanie baz danych, np. {app1 = "app1_db", app2 = "app2_db"}
  identifier             = "${each.key}-instance"  # Unikalna nazwa instancji
  allocated_storage      = 30                      # Ilość GB miejsca na dysku
  engine                 = "postgres"              # Silnik bazy danych
  engine_version         = "15"                    # Wersja silnika PostgreSQL
  instance_class         = "db.t3.micro"           # Typ instancji
  username               = var.db_user             # Nazwa użytkownika zdefiniowana w zmiennych
  password               = var.db_password         # Hasło użytkownika zdefiniowane w zmiennych
  db_name                = each.value              # Nazwa bazy danych
  db_subnet_group_name   = aws_db_subnet_group.default.name  # Przypisanie do grupy subnetów
  vpc_security_group_ids = [aws_security_group.db_sg.id]     # Przypisanie grupy bezpieczeństwa
  skip_final_snapshot    = true                    # Pominięcie tworzenia migawki przy usuwaniu instancji
  publicly_accessible    = true                    # Udostępnienie instancji publicznie
}
