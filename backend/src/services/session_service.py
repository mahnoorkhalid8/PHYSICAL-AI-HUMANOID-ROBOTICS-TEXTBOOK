import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(src_dir))

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from datetime import datetime
from models.chat_session import ChatSession
from models.message import Message
from logging_config import logger

class SessionService:
    def __init__(self):
        pass

    def create_session(self, db: Session, user_id: Optional[UUID] = None, metadata: Optional[Dict] = None) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            user_id=user_id,
            metadata_=metadata or {}
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        logger.info(f"Created new chat session: {session.id}")
        return session

    def get_session(self, db: Session, session_id: UUID) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        return db.query(ChatSession).filter(ChatSession.id == session_id).first()

    def get_session_messages(self, db: Session, session_id: UUID) -> List[Message]:
        """Get all messages for a specific session"""
        return db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()

    def update_session_metadata(self, db: Session, session_id: UUID, metadata: Dict) -> bool:
        """Update the metadata for a session"""
        session = self.get_session(db, session_id)
        if session:
            session.metadata_ = metadata
            session.updated_at = datetime.utcnow()
            db.commit()
            logger.debug(f"Updated metadata for session: {session_id}")
            return True
        return False

    def validate_session_exists(self, db: Session, session_id: UUID) -> bool:
        """Check if a session exists"""
        session = self.get_session(db, session_id)
        return session is not None

    def get_session_by_user_id(self, db: Session, user_id: UUID) -> List[ChatSession]:
        """Get all sessions for a specific user"""
        return db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.created_at.desc()).all()

    def delete_session(self, db: Session, session_id: UUID) -> bool:
        """Delete a session (soft delete by marking as inactive in a real implementation)"""
        session = self.get_session(db, session_id)
        if session:
            # In a real implementation, you might want to do soft delete
            # For now, we'll just delete completely
            db.delete(session)
            db.commit()
            logger.info(f"Deleted session: {session_id}")
            return True
        return False

    def update_session_timestamp(self, db: Session, session_id: UUID) -> bool:
        """Update the updated_at timestamp for a session"""
        session = self.get_session(db, session_id)
        if session:
            session.updated_at = datetime.utcnow()
            db.commit()
            logger.debug(f"Updated timestamp for session: {session_id}")
            return True
        return False