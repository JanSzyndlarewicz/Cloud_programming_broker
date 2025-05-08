output "db_connection_strings" {
  value = {
    for key, db in aws_db_instance.services :
    key => "postgresql+psycopg2://${db.endpoint}:${db.port}/${db.db_name}"
  }
  sensitive = true
}
