import logging.config
import os
from contextlib import asynccontextmanager

import uvicorn
import yaml
from fastapi import FastAPI

from dining_service.app.api.routers import router
from dining_service.infrastructure.database.init import get_db
from dining_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus
from dining_service.infrastructure.event_bus.setup import setup_event_subscribers

# Load logging configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
logging_config_path = os.path.join(current_dir, "logging.yaml")

with open(logging_config_path, "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application dining is starting up...")

    # Initialize the database session
    db = next(get_db())

    logger.info("Database session initialized.")
    # Initialize the RabbitMQ event bus
    event_bus = RabbitMQEventBus()

    logger.info("RabbitMQ event bus initialized.")

    # Set up event subscribers
    setup_event_subscribers(db, event_bus)

    logger.info("Event subscribers set up.")

    try:
        yield
    finally:
        # Close RabbitMQ connection on shutdown
        event_bus.close()
        logger.info("Application is shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    logger.info("Starting the application...")
    uvicorn.run(app, host="0.0.0.0", port=8000)