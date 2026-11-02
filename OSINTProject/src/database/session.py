from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from .models import Base

# Create the tables in the database
engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a DB session in a FastAPI route
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
