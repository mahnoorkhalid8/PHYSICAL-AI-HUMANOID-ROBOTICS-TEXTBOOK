---
title: Physical AI Humanoid Robotics Textbook Chatbot
emoji: 🤖
colorFrom: blue
colorTo: red
sdk: docker
app_port: 8000
pinned: false
license: mit
---

# Physical AI Humanoid Robotics Textbook

An interactive textbook for Physical AI and Humanoid Robotics with an integrated RAG (Retrieval-Augmented Generation) chatbot for enhanced learning.

## Overview

This application provides an interactive chatbot interface for exploring the Physical AI Humanoid Robotics textbook. It uses RAG (Retrieval-Augmented Generation) to provide accurate, context-aware answers to questions about the textbook content.

## Features

- **Interactive Learning**: Engage with the content through an AI-powered chatbot
- **Context-Aware Queries**: Ask questions about specific content or the entire book
- **Selected Text Queries**: Select text on a page and ask questions about it specifically
- **Session Management**: Conversations persist across page navigation
- **Source Attribution**: Answers include links to relevant textbook sections
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive chat interface**
- **RAG-powered responses based on textbook content**
- **Support for selected text context queries**
- **Authentication and personalization features**
- **Urdu translation capabilities**

## Architecture

The system consists of:

- **Frontend**: Docusaurus-based website with React chatbot widget
- **Backend**: FastAPI server with RAG capabilities
- **Vector Store**: Qdrant for document embeddings
- **Database**: SQLite for session management (can be configured for PostgreSQL)
- **LLM**: Groq API for response generation
- **Authentication**: JWT-based authentication system
- **Translation**: AI-powered Urdu translation capabilities

## How it Works

1. The system uses vector embeddings to index the textbook content
2. When a user asks a question, relevant content is retrieved from the vector database
3. The retrieved context is combined with the user's question and sent to an LLM
4. The LLM generates a response based on the textbook content

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

## Environment Variables

To run this application, you'll need to set the following environment variables:

- `GROQ_API_KEY`: Your Groq API key for LLM access (used for both chatbot responses and Urdu translation)
- `QDRANT_HOST`: Qdrant vector database host (default: localhost)
- `QDRANT_PORT`: Qdrant vector database port (default: 6333)
- `DATABASE_URL`: Database URL (default: sqlite:///./chatbot.db)

## API Configuration

The project connects directly to the backend API in both development and production:

- In development: Frontend connects to `http://localhost:8000/api/query`
- In production: Frontend connects to `${BACKEND_URL}/api/query` using the `BACKEND_URL` environment variable

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

### Manual Setup on Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Choose "Cuda 12.1" or "Base image" as the hardware
4. Add your repository files to the Space
5. The `Dockerfile` and `app.py` in the root directory will be used automatically
6. Add your API keys as Space secrets:
   - `GROQ_API_KEY`: Your Groq API key
   - Other required API keys

### Configuration for Hugging Face Spaces

The backend uses environment variables:
- `GROQ_API_KEY`: Your LLM provider API key
- `BACKEND_HOST`: Host to bind to (default: 0.0.0.0)
- `BACKEND_PORT`: Port to bind to (default: 8000, but Hugging Face will set this automatically)
- `DATABASE_URL`: Database connection string (uses SQLite by default)
- `QDRANT_HOST`: Qdrant vector database host
- `QDRANT_PORT`: Qdrant vector database port

### Notes for Hugging Face Spaces

- The backend will automatically initialize the database on startup
- Textbook content is loaded from the `docs` directory during startup
- The service will be available at `https://your-username.hf.space`

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

## Usage

1. Ask questions about the Physical AI Humanoid Robotics textbook
2. The chatbot will provide answers based on the textbook content
3. Users can sign up/sign in for personalized content
4. Content can be translated to Urdu for better accessibility

## Scaling Considerations

### For Production Use
- Consider using PostgreSQL instead of SQLite
- Consider using a dedicated Qdrant instance instead of the local one
- Monitor API usage for your LLM provider
- Set up proper logging and monitoring

## Troubleshooting

### Backend Issues
- Ensure all required environment variables (API keys) are set as Space secrets
- Check the Hugging Face Space logs for errors
- Verify that the database initialized correctly
- Check that the Qdrant connection is working properly