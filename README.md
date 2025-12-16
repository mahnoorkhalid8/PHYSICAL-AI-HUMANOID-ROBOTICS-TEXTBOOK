# Physical AI Humanoid Robotics Textbook

An interactive textbook for Physical AI and Humanoid Robotics with an integrated RAG (Retrieval-Augmented Generation) chatbot for enhanced learning.

## Features

- **Interactive Learning**: Engage with the content through an AI-powered chatbot
- **Context-Aware Queries**: Ask questions about specific content or the entire book
- **Selected Text Queries**: Select text on a page and ask questions about it specifically
- **Session Management**: Conversations persist across page navigation
- **Source Attribution**: Answers include links to relevant textbook sections
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Architecture

The system consists of:

- **Frontend**: Docusaurus-based website with React chatbot widget
- **Proxy Layer**: Next.js API routes that forward requests to backend (handles CORS)
- **Backend**: FastAPI server with RAG capabilities
- **Vector Store**: Qdrant for document embeddings
- **Database**: Postgres/SQLite for session management

## Prerequisites

- **Node.js 18+** for the frontend/Docusaurus application
- **Python 3.11+** for the backend FastAPI application
- **Qdrant** vector database
- **PostgreSQL** database (or SQLite for development)
- **API keys** for your chosen LLM provider (OpenAI, Gemini, Groq, etc.)

## Setup and Running

For detailed setup and running instructions, see [RUNNING.md](RUNNING.md).

Quick start:
1. Install dependencies: `npm install` (frontend) and `pip install -r requirements.txt` (backend)
2. Set up environment variables in `.env.local`
3. Start the backend: `cd backend && uvicorn src.main:app --reload`
4. Ingest textbook content: `cd backend/src && python ingest.py`
5. Start the frontend: `npm run start`

## API Proxy Configuration

The project includes a proxy configuration for handling API requests in production:

- Frontend makes requests to `/api/query`
- Vercel rewrites these to `/api/proxy`
- The proxy forwards requests to the actual backend at `BACKEND_URL`
- This resolves CORS issues when deployed

## Scripts

Useful scripts are available in the `scripts/` folder:
- `setup.sh`/`setup.bat` - Install dependencies for both frontend and backend
- `dev-start.sh`/`dev-start.bat` - Start both backend and frontend for development

## Documentation

- [Chatbot Integration](docs/chatbot-integration.mdx) - Detailed documentation about the chatbot implementation
- [RUNNING.md](RUNNING.md) - Complete setup and running instructions
- [API Documentation](backend/docs/api.md) - Backend API documentation

## Project Structure

- `backend/` - FastAPI backend with RAG functionality
- `docs/` - Docusaurus documentation pages
- `src/` - Custom React components and utilities
- `scripts/` - Setup and development scripts
- `specs/` - Feature specifications and plans
- `history/` - Project history and prompt records