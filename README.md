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
- **Backend**: FastAPI server with RAG capabilities
- **Vector Store**: Qdrant for document embeddings
- **Database**: SQLite for session management

## Deployment

### Frontend (Vercel)

1. Push your code to a GitHub repository
2. Go to [Vercel](https://vercel.com) and connect your GitHub repository
3. In the Vercel dashboard, set the following environment variable:
   - `BACKEND_URL`: The URL of your deployed backend (e.g., `https://your-backend-app.hf.space`)
4. Vercel will automatically detect this is a Docusaurus project and build it

### Backend (Hugging Face Spaces)

The backend is configured for deployment on Hugging Face Spaces:

1. Create a new Space on Hugging Face
2. Set the Space to use Docker
3. Use the provided `Dockerfile` and `app.py` files
4. The backend will be deployed and accessible at your Space URL

## Prerequisites

- **Node.js 18+** for the frontend/Docusaurus application
- **Python 3.11+** for the backend FastAPI application
- **Qdrant** vector database
- **SQLite** database (or PostgreSQL for production)
- **API keys** for your chosen LLM provider (OpenAI, Gemini, Groq, etc.)

## Setup and Running

For detailed setup and running instructions, see [RUNNING.md](RUNNING.md).

Quick start:
1. Install dependencies: `npm install` (frontend) and `pip install -r requirements.txt` (backend)
2. Set up environment variables in `.env` (backend) and Vercel dashboard (frontend)
3. Start the backend: `cd backend && python -m src.main`
4. Ingest textbook content: `cd backend/src && python ingest.py`
5. Start the frontend: `npm run start`

## API Configuration

The project connects directly to the backend API in both development and production:

- In development: Frontend connects to `http://localhost:8000/api/query`
- In production: Frontend connects to `${BACKEND_URL}/api/query` using the `BACKEND_URL` environment variable

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
- `specs/` - Feature specifications and plans
- `history/` - Project history and prompt records