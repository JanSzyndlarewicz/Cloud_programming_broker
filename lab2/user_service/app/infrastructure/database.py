from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Konfiguracja bazy danych - tutaj przykład dla SQLite (zmień na odpowiednią bazę danych)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Możesz zmienić na swoją bazę danych

# Tworzymy silnik bazy danych
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # Tylko dla SQLite

# Sesja bazy danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Podstawowa klasa dla wszystkich modeli
Base = declarative_base()

# Funkcja do uzyskiwania sesji DB w aplikacji
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
