from infrastructure.config import Config
from infrastructure.database.models import Base, Room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(Config.DATABASE_URL)

# Najpierw usuwamy wszystkie istniejące tabele, potem tworzymy nowe
Base.metadata.drop_all(bind=engine)
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
                Room(number="201", price_per_night=150.0)
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