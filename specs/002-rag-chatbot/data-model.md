# Data Model: RAG Chatbot for Existing Book

**Feature**: RAG Chatbot for Existing Book
**Date**: 2025-12-10
**Branch**: 002-rag-chatbot

## Entity Models

### ChatSession
- **Description**: Represents a user's conversation session with the chatbot
- **Fields**:
  - id: UUID (primary key)
  - created_at: DateTime (timestamp when session started)
  - updated_at: DateTime (timestamp of last activity)
  - user_id: UUID (optional, for logged-in users)
  - metadata: JSON (additional session information)
- **Relationships**:
  - One-to-many with Message entities
- **Validation**:
  - created_at must be in the past
  - updated_at must be >= created_at

### Message
- **Description**: An individual message in a conversation
- **Fields**:
  - id: UUID (primary key)
  - session_id: UUID (foreign key to ChatSession)
  - role: String (either "user" or "assistant")
  - content: Text (the actual message content)
  - timestamp: DateTime (when message was created)
  - context_used: JSON (book sections referenced in the response)
- **Relationships**:
  - Many-to-one with ChatSession
- **Validation**:
  - role must be either "user" or "assistant"
  - content must not be empty
  - timestamp must be in chronological order within session

### QueryContext
- **Description**: Information about the context of a query
- **Fields**:
  - id: UUID (primary key)
  - query_text: Text (the original user query)
  - selected_text: Text (optional, text selected by user)
  - page_context: String (optional, current page URL or identifier)
  - search_scope: String (either "full_book", "selected_text", or "current_page")
  - embedding_metadata: JSON (information about vector search)
- **Relationships**:
  - One-to-one with Message (via message.context_used)
- **Validation**:
  - search_scope must be one of the allowed values
  - selected_text and page_context are optional but at least one should be provided if not full_book

### VectorEmbedding
- **Description**: Represents embedded content from the textbook for RAG
- **Fields**:
  - id: UUID (primary key)
  - content: Text (the original text content)
  - embedding_vector: Array<Float> (vector representation of content)
  - content_type: String (e.g., "chapter", "section", "paragraph")
  - source_document: String (which book section this comes from)
  - metadata: JSON (additional information like page numbers, headings)
- **Relationships**:
  - Stored in Qdrant vector database rather than Postgres
- **Validation**:
  - embedding_vector must have consistent dimensions
  - content must not be empty

## State Transitions

### ChatSession States
- **Active**: New session created, ready for messages
- **Active with messages**: Session has at least one message
- **Inactive**: Session has not been updated for a specified period (e.g., 24 hours)
- **Archived**: Session has been marked for archival after inactivity

### Message States
- **Pending**: Message submitted, waiting for processing
- **Processing**: Backend is generating response
- **Completed**: Response generated and returned to user
- **Error**: Error occurred during processing

## Relationships

```
ChatSession (1) ←→ (Many) Message
Message (1) ←→ (1) QueryContext
VectorEmbedding (Many) → Search/Query operations
```

## Constraints

- **Session Expiration**: Sessions inactive for 24 hours may be archived
- **Message Limits**: Maximum number of messages per session (e.g., 100) to prevent excessive storage
- **Content Length**: Maximum content length for messages (e.g., 10,000 characters)
- **Embedding Limits**: Vector embeddings have maximum dimension constraints based on Qdrant capabilities
- **Foreign Key Constraints**: All foreign key relationships must reference existing records

## Indexes

- ChatSession.created_at (for chronological queries)
- ChatSession.updated_at (for activity-based queries)
- Message.session_id (for session-based queries)
- Message.timestamp (for chronological ordering)
- VectorEmbedding.source_document (for document-based queries)