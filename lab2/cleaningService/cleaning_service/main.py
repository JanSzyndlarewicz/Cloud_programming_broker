import logging.config
import os
from contextlib import asynccontextmanager

import uvicorn
import yaml
from app.api.routers import router
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.messaging.setup import setup_event_subscribers
from infrastructure.persistence import get_db
from fastapi import FastAPI

# Load logging configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
logging_config_path = os.path.join(current_dir, "logging.yaml")

with open(logging_config_path, "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application cleaning is starting up...")

    db = next(get_db())
    event_bus = RabbitMQEventBus()

    logger.info("RabbitMQ event bus initialized.")

    # Set up event subscribers
    setup_event_subscribers(db, event_bus)

    logger.info("Event subscribers set up.")

    try:
        yield
    finally:
        event_bus.close()
        logger.info("Application is shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    logger.info("Starting the application...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
