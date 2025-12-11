# Quickstart Guide: RAG Chatbot for Existing Book

**Feature**: RAG Chatbot for Existing Book
**Date**: 2025-12-10
**Branch**: 002-rag-chatbot

## Prerequisites

- Python 3.11+ for backend services
- Node.js 18+ for frontend development
- Qdrant vector database instance
- Neon Postgres database
- OpenAI API key (or alternative LLM provider)

## Environment Setup

### Backend Dependencies
```bash
pip install fastapi uvicorn python-multipart qdrant-client openai psycopg2-binary python-dotenv
```

### Frontend Dependencies
```bash
npm install react react-dom
# Additional dependencies will be added during implementation
```

### Environment Variables
Create a `.env` file with the following variables:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=book_embeddings

# Postgres Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/chatbot_db

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4 if preferred

# Application Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001", "https://yourdomain.com"]
```

## Database Setup

### Postgres Schema
The application requires the following tables:

```sql
-- Chat sessions table
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID,
    metadata JSONB
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    context_used JSONB
);
```

### Qdrant Collection
Create a Qdrant collection for storing book embeddings:

```python
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)
client.create_collection(
    collection_name="book_embeddings",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # Assuming OpenAI embeddings
)
```

## Running the Application

### Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend/

# Start the development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

### Frontend Integration
The React chatbot component can be integrated into Docusaurus MDX pages:

```jsx
// Example integration in MDX
import ChatbotWidget from '@site/src/components/ChatbotWidget';

<ChatbotWidget />
```

## API Usage Examples

### Query the RAG System
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain ROS2 architecture for humanoid robots",
    "selected_text": "The ROS2 architecture provides a flexible framework...",
    "context": {
      "page_url": "/docs/01-robotic-nervous-system/ros2-architecture",
      "search_scope": "selected_text"
    }
  }'
```

### Create a New Session
```bash
curl -X POST http://localhost:8000/api/session \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "user_agent": "Mozilla/5.0...",
      "page_url": "/docs/01-robotic-nervous-system"
    }
  }'
```

## Development Workflow

1. **Start Qdrant**: Ensure Qdrant vector database is running
2. **Start Postgres**: Ensure Neon Postgres connection is available
3. **Load Book Data**: Run the ingestion script to load book content into Qdrant
4. **Start Backend**: Run the FastAPI application
5. **Integrate Frontend**: Add the React component to MDX pages
6. **Test**: Verify the end-to-end functionality

## Testing

### Backend Tests
```bash
# Run backend tests
pytest tests/ -v
```

### Frontend Tests
```bash
# Run frontend tests
npm test
```

## Building for Production

### Backend
```bash
# Create production build
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Frontend Integration
The React component will be bundled with the Docusaurus build process.

## Troubleshooting

### Common Issues

1. **Qdrant Connection**: Verify Qdrant is running and accessible at the configured host/port
2. **Database Connection**: Check that Postgres credentials and connection string are correct
3. **API Keys**: Ensure OpenAI or other LLM provider API keys are properly configured
4. **CORS Issues**: Verify that the frontend origin is included in CORS settings