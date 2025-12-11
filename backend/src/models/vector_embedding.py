from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID

class VectorEmbedding(BaseModel):
    """
    Pydantic model to represent vector embeddings stored in Qdrant.
    These are not stored in Postgres but in the Qdrant vector database.
    """
    id: int  # Qdrant point ID
    content: str
    embedding_vector: List[float]
    content_type: str  # e.g., "chapter", "section", "paragraph"
    source_document: str  # which book section this comes from
    metadata: Optional[Dict[str, Any]] = None
    score: Optional[float] = None  # similarity score from search results

    class Config:
        # Allow extra fields in case Qdrant returns additional metadata
        extra = "allow"

class SearchQuery(BaseModel):
    """
    Model for search queries to Qdrant
    """
    query_text: str
    top_k: int = 5  # number of results to return
    search_scope: str = "full_book"  # "full_book", "selected_text", "current_page"
    selected_text: Optional[str] = None
    page_context: Optional[str] = None