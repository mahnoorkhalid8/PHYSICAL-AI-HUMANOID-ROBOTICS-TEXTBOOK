from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(src_dir))

from db import get_db
from services.chat_service import ChatService
from models.message import Message
from logging_config import logger

router = APIRouter()

# Pydantic models for session requests/responses
class CreateSessionRequest(BaseModel):
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class CreateSessionResponse(BaseModel):
    session_id: str
    created_at: str

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str

class GetMessagesResponse(BaseModel):
    messages: List[MessageResponse]

class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[Dict[str, Any]] = None

# Initialize service
chat_service = ChatService()

@router.post("/session",
             response_model=CreateSessionResponse,
             responses={
                 201: {"description": "Session created successfully"},
                 400: {"model": ErrorResponse, "description": "Bad request"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def create_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_db)
):
    """
    Creates a new chat session.
    """
    try:
        logger.info("Creating new chat session")

        # Convert string user_id to UUID if provided
        user_id_uuid = None
        if request.user_id:
            try:
                user_id_uuid = uuid.UUID(request.user_id)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "INVALID_USER_ID",
                        "code": "INVALID_INPUT",
                        "details": {"message": "user_id must be a valid UUID"}
                    }
                )

        # Create session using the service
        session = chat_service.create_session(
            db=db,
            user_id=user_id_uuid,
            metadata=request.metadata
        )

        response = CreateSessionResponse(
            session_id=str(session.id),
            created_at=session.created_at.isoformat() + "Z"
        )

        logger.info(f"Successfully created session: {session.id}")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "SESSION_CREATION_ERROR",
                "code": "INTERNAL_ERROR",
                "details": {"message": str(e)}
            }
        )

@router.get("/session/{session_id}/messages",
            response_model=GetMessagesResponse,
            responses={
                200: {"description": "Messages retrieved successfully"},
                400: {"model": ErrorResponse, "description": "Bad request"},
                404: {"model": ErrorResponse, "description": "Session not found"},
                500: {"model": ErrorResponse, "description": "Internal server error"}
            })
async def get_session_messages(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves messages for a specific session.
    """
    try:
        logger.info(f"Retrieving messages for session: {session_id}")

        # Validate session_id format
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "INVALID_SESSION_ID",
                    "code": "INVALID_INPUT",
                    "details": {"message": "session_id must be a valid UUID"}
                }
            )

        # Get the session to verify it exists
        session = chat_service.get_session(db, session_uuid)
        if not session:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "SESSION_NOT_FOUND",
                    "code": "NOT_FOUND",
                    "details": {"message": f"Session with id {session_id} not found"}
                }
            )

        # Get messages for the session
        messages = chat_service.get_messages(db, session_uuid)

        # Convert to response format
        message_responses = []
        for msg in messages:
            message_responses.append(MessageResponse(
                id=str(msg.id),
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp.isoformat() + "Z"
            ))

        response = GetMessagesResponse(
            messages=message_responses
        )

        logger.info(f"Successfully retrieved {len(messages)} messages for session: {session_id}")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving session messages: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "MESSAGES_RETRIEVAL_ERROR",
                "code": "INTERNAL_ERROR",
                "details": {"message": str(e)}
            }
        )

@router.get("/session/health")
async def session_health():
    """
    Health check for the session endpoint
    """
    return {"status": "session endpoint is healthy"}