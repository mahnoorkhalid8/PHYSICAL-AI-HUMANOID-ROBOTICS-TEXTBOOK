from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from datetime import datetime
from ..models.chat_session import ChatSession
from ..models.message import Message
from ..models.query_context import QueryContext
from ..logging_config import logger

class ChatService:
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

    def create_message(self, db: Session, session_id: UUID, role: str, content: str, context_used: Optional[Dict] = None) -> Message:
        """Create a new message in a session"""
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            context_used=context_used or {}
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        logger.debug(f"Created message in session {session_id} with role {role}")
        return message

    def get_messages(self, db: Session, session_id: UUID) -> List[Message]:
        """Get all messages for a session"""
        return db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()

    def create_query_context(self, db: Session, query_text: str, selected_text: Optional[str] = None,
                           page_context: Optional[str] = None, search_scope: str = "full_book",
                           embedding_metadata: Optional[Dict] = None) -> QueryContext:
        """Create a query context record"""
        query_context = QueryContext(
            query_text=query_text,
            selected_text=selected_text,
            page_context=page_context,
            search_scope=search_scope,
            embedding_metadata=embedding_metadata or {}
        )
        db.add(query_context)
        db.commit()
        db.refresh(query_context)
        logger.debug(f"Created query context for query: {query_text[:50]}...")
        return query_context

    def validate_role(self, role: str) -> bool:
        """Validate that the role is either 'user' or 'assistant'"""
        return role in ["user", "assistant"]

    def update_session_timestamp(self, db: Session, session_id: UUID) -> None:
        """Update the updated_at timestamp for a session"""
        session = self.get_session(db, session_id)
        if session:
            session.updated_at = datetime.utcnow()
            db.commit()
            logger.debug(f"Updated timestamp for session: {session_id}")

    def get_session_history(self, db: Session, session_id: UUID, limit: Optional[int] = None) -> List[Message]:
        """Get session history with optional limit"""
        query = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp.desc())
        if limit:
            query = query.limit(limit)
        messages = query.all()
        # Return in chronological order (oldest first)
        return list(reversed(messages))