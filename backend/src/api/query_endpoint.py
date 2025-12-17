
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from ..db import get_db
from ..services.chat_service import ChatService
from ..services.rag_service import RAGService
from ..logging_config import logger

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

        # Validate search scope
        if search_scope not in ["full_book", "selected_text", "current_page"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "INVALID_SEARCH_SCOPE",
                    "code": "INVALID_INPUT",
                    "details": {"message": f"search_scope must be one of: full_book, selected_text, current_page. Got: {search_scope}"}
                }
            )

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
        if len(request.question) > 1000:  # Set a reasonable limit
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "QUESTION_TOO_LONG",
                    "code": "INVALID_INPUT",
                    "details": {"message": "Question is too long (max 1000 characters)"}
                }
            )

        # Validate selected_text length if provided
        if request.selected_text and len(request.selected_text) > 5000:  # Set a reasonable limit
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "SELECTED_TEXT_TOO_LONG",
                    "code": "INVALID_INPUT",
                    "details": {"message": "Selected text is too long (max 5000 characters)"}
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
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "error": "SESSION_NOT_FOUND",
                            "code": "NOT_FOUND",
                            "details": {"message": f"Session with id {request.session_id} not found"}
                        }
                    )
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "INVALID_SESSION_ID",
                        "code": "INVALID_INPUT",
                        "details": {"message": "session_id must be a valid UUID"}
                    }
                )

        # Process the RAG query
        result = rag_service.process_query(
            query=request.question,
            selected_text=request.selected_text,
            search_scope=search_scope
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

        # Update the response with current timestamp
        result["timestamp"] = datetime.utcnow().isoformat() + "Z"

        logger.info(f"Successfully completed query: {request.question[:50]}...")
        return QueryResponse(**result)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in query endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "QUERY_PROCESSING_ERROR",
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