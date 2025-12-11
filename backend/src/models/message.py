from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.mutable import MutableDict
from ..db import Base
from datetime import datetime
import uuid

class Message(Base):
    __tablename__ = "messages"

    # Use string type for UUID to work with both SQLite and PostgreSQL
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)  # Store as string to work with SQLite
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    context_used = Column(MutableDict.as_mutable(JSON), default=dict)

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, timestamp={self.timestamp})>"