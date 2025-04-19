from cleaning_service.infrastructure.config import Config
from cleaning_service.infrastructure.database.models import Base, Room, RoomStatus, Cleaning
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the database engine
engine = create_engine(Config.DATABASE_URL)

# Drop all existing tables and create new ones
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize sample data
def initialize_data():
    db = SessionLocal()
    try:
        # Check if rooms already exist
        if not db.query(Room).first():
            # Add some sample rooms
            rooms = [
                Room(number="101"),
                Room(number="102"),
                Room(number="201"),
            ]
            db.add_all(rooms)
            db.commit()
    finally:
        db.close()

# Initialize the sample data
initialize_data()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()