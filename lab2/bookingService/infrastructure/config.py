import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "booking_db")

    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "events")

    DATABASE_URL = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
