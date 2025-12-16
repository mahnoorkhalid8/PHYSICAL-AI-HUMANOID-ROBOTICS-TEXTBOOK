# Running the Physical AI Humanoid Robotics Textbook Project

This guide explains how to set up and run the Physical AI Humanoid Robotics Textbook project with the RAG chatbot functionality.

## Prerequisites

- **Node.js 18+** for the frontend/Docusaurus application
- **Python 3.11+** for the backend FastAPI application
- **Qdrant** vector database
- **PostgreSQL** database (or SQLite for development)
- **API keys** for your chosen LLM provider (OpenAI, Gemini, Groq, etc.)

## Setup

### 1. Environment Configuration

Create a `.env.local` file in the project root with the following variables:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=book_embeddings
# Add your Qdrant API key and cluster endpoint if using cloud

# Database Configuration
DATABASE_URL=sqlite:///./chatbot.db
# Or PostgreSQL URL if using Postgres

# LLM Provider Configuration
OPENAI_API_KEY=your_openai_api_key_here  # or GEMINI_API_KEY, GROQ_API_KEY, etc.
OPENAI_MODEL=gpt-3.5-turbo  # or your preferred model

# Application Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001", "https://yourdomain.com"]

# Proxy Configuration (for Vercel deployment)
BACKEND_URL=http://localhost:8000
```

### 2. Install Dependencies

For the frontend (in project root):
```bash
npm install
```

For the backend (in `backend` directory):
```bash
cd backend
pip install -r requirements.txt
```

Or use the setup script:
```bash
./scripts/setup.sh  # Unix/Linux/Mac
# or
scripts\setup.bat   # Windows
```

## Running the Application

### 1. Start the Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend (Docusaurus)

In a separate terminal:
```bash
npm run start
```

Or use the development start script:
```bash
./scripts/dev-start.sh  # Unix/Linux/Mac
# or
scripts\dev-start.bat   # Windows
```

### 3. Ingest the Textbook Content

Before using the chatbot, you need to ingest the textbook content into the vector database:

```bash
cd backend/src
python ingest.py
```

## API Proxy Configuration

The project includes a proxy configuration for handling API requests in production:

- Frontend makes requests to `/api/query`
- Vercel rewrites these to `/api/proxy`
- The proxy forwards requests to the actual backend at `BACKEND_URL`
- This resolves CORS issues when deployed

## Development Notes

- The chatbot widget is integrated into the Docusaurus site
- Selected text on pages can be sent to the chatbot for context-aware responses
- Session data persists across page navigation
- The system uses vector embeddings for RAG (Retrieval-Augmented Generation)

## Troubleshooting

1. **Backend not accessible**: Ensure the backend server is running on the configured port
2. **CORS errors**: Check that `BACKEND_URL` is properly set in environment variables
3. **Chatbot not responding**: Verify that the vector database has been populated with textbook content
4. **API keys**: Ensure all required API keys are properly configured in environment variables

## Production Deployment

For production deployment to Vercel:

1. Set the `BACKEND_URL` environment variable to your production backend URL
2. The `vercel.json` configuration will handle API request proxying automatically
3. Ensure your backend is deployed and accessible at the configured URL