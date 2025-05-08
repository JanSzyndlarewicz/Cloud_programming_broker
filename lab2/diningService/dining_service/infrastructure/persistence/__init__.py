from infrastructure.config.settings import Config
from infrastructure.persistence.models.orm_dining_reservation import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the persistence engine
engine = create_engine(Config.DATABASE_URL)

# Drop all existing tables and create new ones
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get a persistence session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
