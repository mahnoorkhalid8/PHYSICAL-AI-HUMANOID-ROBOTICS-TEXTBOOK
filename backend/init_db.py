#!/usr/bin/env python
"""
Script to initialize the database tables for the chatbot application.
This creates the necessary tables for SQLite without requiring alembic.
"""
import sys
import os
from pathlib import Path

# Add the backend/src to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.db import Base, engine
from src.models.chat_session import ChatSession
from src.models.message import Message
from src.models.query_context import QueryContext  # Import if exists
from src.models.vector_embedding import VectorEmbedding  # Import if exists
from src.logging_config import logger

def init_db():
    """Initialize the database tables"""
    print("Initializing database tables...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Database tables created successfully!")

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables created: {tables}")

        return True
    except Exception as e:
        print(f"[ERROR] Error creating database tables: {e}")
        logger.error(f"Error creating database tables: {e}")
        return False

if __name__ == "__main__":
    success = init_db()
    if success:
        print("\nDatabase initialization completed successfully!")
    else:
        print("\nDatabase initialization failed!")
        sys.exit(1)