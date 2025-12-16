import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(src_dir))

from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableDict
from db import Base
import uuid

class QueryContext(Base):
    __tablename__ = "query_contexts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    page_context = Column(String, nullable=True)
    search_scope = Column(String(20), nullable=False)  # 'full_book', 'selected_text', or 'current_page'
    embedding_metadata = Column(MutableDict.as_mutable(JSON), default=dict)

    def __repr__(self):
        return f"<QueryContext(id={self.id}, query_text='{self.query_text[:50]}...', search_scope={self.search_scope})>"