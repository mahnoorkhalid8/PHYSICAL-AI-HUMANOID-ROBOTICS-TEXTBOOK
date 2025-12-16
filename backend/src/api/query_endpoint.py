from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID
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
from services.rag_service import RAGService
from logging_config import logger
import traceback

router = APIRouter()

# Pydantic models for request/response
class QueryContext(BaseModel):
    page_url: Optional[str] = None
    search_scope: str = Field(default="full_book", description="enum: 'full_book', 'selected_text', 'current_page'")

class QueryRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    context: Optional[QueryContext] = None
    session_id: Optional[str] = None

class Source(BaseModel):
    title: str
    url: str
    relevance_score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    query_id: str
    timestamp: str
    session_id: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[Dict[str, Any]] = None

# Initialize services
chat_service = ChatService()
rag_service = RAGService()

@router.post("/query",
             response_model=QueryResponse,
             responses={
                 200: {"description": "Successful response"},
                 400: {"model": ErrorResponse, "description": "Bad request"},
                 422: {"model": ErrorResponse, "description": "Validation Error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def query_endpoint(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Initiates a RAG-based query against the textbook content.
    """
    try:
        logger.info(f"Processing query: {request.question[:50]}...")

        # Set default context if not provided
        if request.context is None:
            request.context = QueryContext()

        # Set default search scope if not provided
        search_scope = request.context.search_scope or "full_book"

        # Validate search scope (Soft validation)
        valid_scopes = ["full_book", "selected_text", "current_page"]
        if search_scope not in valid_scopes:
            logger.warning(f"Invalid search scope received: {search_scope}. Defaulting to full_book.")
            search_scope = "full_book"

        # Validate question is not empty
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "EMPTY_QUESTION",
                    "code": "INVALID_INPUT",
                    "details": {"message": "Question cannot be empty"}
                }
            )

        # Validate question length
        if len(request.question) > 2000:  # Increased limit
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "QUESTION_TOO_LONG",
                    "code": "INVALID_INPUT",
                    "details": {"message": "Question is too long (max 2000 characters)"}
                }
            )

        # Validate session_id if provided
        session_id = None
        if request.session_id:
            try:
                session_id = UUID(request.session_id)
                # Verify session exists
                existing_session = chat_service.get_session(db, session_id)
                if not existing_session:
                    logger.warning(f"Session {request.session_id} not found. A new session will be created.")
                    session_id = None # Treat as new session
            except ValueError:
                 logger.warning(f"Invalid session_id format: {request.session_id}. A new session will be created.")
                 session_id = None

        # Process the RAG query
        try:
            result = rag_service.process_query(
                query=request.question,
                selected_text=request.selected_text,
                search_scope=search_scope
            )
        except Exception as e:
            logger.error(f"RAG Service Error: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "RAG_SERVICE_ERROR",
                    "code": "INTERNAL_ERROR",
                    "details": {"message": f"Error processing query: {str(e)}"}
                }
            )

        # Use existing session if provided, otherwise create a new one
        if session_id:
            session = existing_session
        else:
            # Create a new session
            session = chat_service.create_session(db)
            # Update result to include the new session ID
            result["session_id"] = str(session.id)

        # Store the query in the session
        try:
            chat_service.create_message(
                db=db,
                session_id=session.id,
                role="user",
                content=request.question
            )

            # Store the response in the session
            chat_service.create_message(
                db=db,
                session_id=session.id,
                role="assistant",
                content=result["answer"]
            )
            
            # Update the session timestamp
            chat_service.update_session_timestamp(db, session.id)
            
        except Exception as db_e:
            logger.error(f"Database Error saving messages: {str(db_e)}")
            # We don't fail the request if DB logging fails, just log it
        
        # Update the response with current timestamp
        result["timestamp"] = datetime.utcnow().isoformat() + "Z"

        logger.info(f"Successfully completed query: {request.question[:50]}...")
        return QueryResponse(**result)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unhandled Error in query endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "error": "UNHANDLED_ERROR",
                "code": "INTERNAL_ERROR",
                "details": {"message": str(e)}
            }
        )

@router.get("/query/health")
async def query_health():
    """
    Health check for the query endpoint
    """
    return {"status": "query endpoint is healthy"}