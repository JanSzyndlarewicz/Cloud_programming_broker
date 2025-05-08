variable "aws_region" {
  default = "us-east-1"
}

variable "db_user" {
  default = "janszyndlarewicz"
}

variable "db_password" {
  default = "haslomaslo"
}

variable "dbs" {
  type = map(string)
  default = {
    booking-db      = "bookingdb"
    cleaning-db     = "cleaningdb"
    dining-db       = "diningdb"
    accounting-db   = "accountingdb"
    notification-db = "notificationdb"
  }
}

variable "aws_account_id" {
  default     = "654654340788"
}