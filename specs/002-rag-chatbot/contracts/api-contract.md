# API Contract: RAG Chatbot for Existing Book

**Feature**: RAG Chatbot for Existing Book
**Date**: 2025-12-10
**Version**: 1.0

## Query Endpoint

### POST /api/query

Initiates a RAG-based query against the textbook content.

#### Request

**Content-Type**: `application/json`

**Body**:
```json
{
  "question": "string",
  "selected_text": "string (optional)",
  "context": {
    "page_url": "string (optional)",
    "search_scope": "enum: 'full_book', 'selected_text', 'current_page' (optional, default: 'full_book')"
  }
}
```

**Parameters**:
- `question`: The user's question about the textbook content
- `selected_text`: Optional text that the user has selected on the page (context for more targeted answers)
- `context.page_url`: Optional URL of the current page (for context awareness)
- `context.search_scope`: Scope of the search (default: 'full_book')

#### Response

**Success Response (200 OK)**:
```json
{
  "answer": "string",
  "sources": [
    {
      "title": "string",
      "url": "string",
      "relevance_score": "number (0-1)"
    }
  ],
  "query_id": "string (UUID)",
  "timestamp": "string (ISO 8601)"
}
```

**Error Response (400 Bad Request)**:
```json
{
  "error": "string",
  "code": "string",
  "details": "object (optional)"
}
```

**Error Response (500 Internal Server Error)**:
```json
{
  "error": "string",
  "code": "INTERNAL_ERROR"
}
```

#### Examples

**Request**:
```json
{
  "question": "Explain ROS2 architecture for humanoid robots",
  "selected_text": "The ROS2 architecture provides a flexible framework...",
  "context": {
    "page_url": "/docs/01-robotic-nervous-system/ros2-architecture",
    "search_scope": "selected_text"
  }
}
```

**Response**:
```json
{
  "answer": "ROS2 (Robot Operating System 2) provides a flexible framework for writing robot software...",
  "sources": [
    {
      "title": "ROS 2 Architecture for Humanoids",
      "url": "/docs/01-robotic-nervous-system/ros2-architecture",
      "relevance_score": 0.95
    }
  ],
  "query_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "timestamp": "2025-12-10T10:30:00Z"
}
```

## Session Management

### POST /api/session

Creates a new chat session.

#### Request

**Content-Type**: `application/json`

**Body**:
```json
{
  "user_id": "string (optional)",
  "metadata": "object (optional)"
}
```

#### Response

**Success Response (201 Created)**:
```json
{
  "session_id": "string (UUID)",
  "created_at": "string (ISO 8601)"
}
```

### GET /api/session/{session_id}/messages

Retrieves messages for a specific session.

#### Response

**Success Response (200 OK)**:
```json
{
  "messages": [
    {
      "id": "string (UUID)",
      "role": "enum: 'user', 'assistant'",
      "content": "string",
      "timestamp": "string (ISO 8601)"
    }
  ]
}
```

## Error Codes

- `INVALID_INPUT`: Request body validation failed
- `VECTOR_STORE_UNAVAILABLE`: Qdrant vector store is temporarily unavailable
- `QUERY_PROCESSING_ERROR`: Error occurred during query processing
- `SESSION_NOT_FOUND`: Specified session does not exist
- `INTERNAL_ERROR`: Unexpected server error