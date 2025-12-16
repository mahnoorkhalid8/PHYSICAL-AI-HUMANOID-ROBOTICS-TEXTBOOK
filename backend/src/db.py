import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(src_dir))

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Database setup - supports both SQLite and PostgreSQL
DATABASE_URL = settings.database_url

# For SQLite, we need to ensure the file path exists and use appropriate flags
if DATABASE_URL.startswith("sqlite"):
    # Add query parameters for SQLite to handle concurrency issues
    if "?charset" not in DATABASE_URL:
        DATABASE_URL += "?charset=utf8"

# Create engine with appropriate settings based on database type
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Required for SQLite with FastAPI
        pool_pre_ping=True  # Verify connections before use
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()