import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(src_dir))

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.mutable import MutableDict
from db import Base
from datetime import datetime
import uuid

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    # Use string type for UUID to work with both SQLite and PostgreSQL
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String(36), nullable=True)  # Store as string to work with SQLite
    metadata_ = Column("metadata", MutableDict.as_mutable(JSON), default=dict)

    def __repr__(self):
        return f"<ChatSession(id={self.id}, created_at={self.created_at})>"