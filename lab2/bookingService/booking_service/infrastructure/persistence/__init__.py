from booking_service.infrastructure.config.settings import Config
from booking_service.infrastructure.persistence.models.orm_room import Base, Room
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine(Config.DATABASE_URL)

# Drop all tables with CASCADE to handle dependencies
# with engine.begin() as connection:
#     # Use text() to create an executable SQL statement
#     connection.execute(text("DROP TABLE IF EXISTS bookings CASCADE"))
#     connection.execute(text("DROP TABLE IF EXISTS rooms CASCADE"))
# # Now create all tables
Base.metadata.drop_all(bind=engine, checkfirst=True)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_data():
    db = SessionLocal()
    try:
        # Check if rooms already exist
        if not db.query(Room).first():
            # Add some sample rooms
            rooms = [
                Room(number="101", price_per_night=100.0),
                Room(number="102", price_per_night=120.0),
                Room(number="201", price_per_night=150.0),
            ]
            db.add_all(rooms)
            db.commit()
    finally:
        db.close()


initialize_data()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
