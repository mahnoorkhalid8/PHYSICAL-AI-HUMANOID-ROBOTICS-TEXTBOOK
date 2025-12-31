---
title: Physical AI Humanoid Robotics Textbook Chatbot
emoji: 🤖
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
license: mit
---

# Physical AI Humanoid Robotics Textbook Chatbot

This is an AI-powered chatbot that helps users understand the Physical AI Humanoid Robotics textbook content using Retrieval-Augmented Generation (RAG).

## Overview

This application provides an interactive chatbot interface for exploring the Physical AI Humanoid Robotics textbook. It uses RAG (Retrieval-Augmented Generation) to provide accurate, context-aware answers to questions about the textbook content.

## Features

- Interactive chat interface
- RAG-powered responses based on textbook content
- Session management to maintain conversation context
- Support for selected text context queries
- Authentication and personalization features
- Urdu translation capabilities

## How it Works

1. The system uses vector embeddings to index the textbook content
2. When a user asks a question, relevant content is retrieved from the vector database
3. The retrieved context is combined with the user's question and sent to an LLM
4. The LLM generates a response based on the textbook content

## Environment Variables

To run this application, you'll need to set the following environment variables as Space secrets:

- `GROQ_API_KEY`: Your Groq API key for LLM access
- `QDRANT_HOST`: Qdrant vector database host (default: localhost)
- `QDRANT_PORT`: Qdrant vector database port (default: 6333)
- `DATABASE_URL`: Database URL (default: sqlite:///./chatbot.db)

## Deployment on Hugging Face Spaces

### Quick Deploy

[![Duplicate this Space](https://huggingface.co/datasets/huggingface/deep-rl-class/resolve/main/imgs/spaces_deploy.png)](https://huggingface.co/spaces/mahnoorkhalid8/physical-ai-humanoid-robotics-textbook-chatbot?duplicate=true)

### Manual Setup

1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Choose "Cuda 12.1" or "Base image" as the hardware
4. Add your repository files to the Space
5. The `Dockerfile` and `app.py` in the root directory will be used automatically
6. Add your API keys as Space secrets:
   - `GROQ_API_KEY`: Your Groq API key
   - Other required API keys

### Configuration

The backend uses environment variables:
- `GROQ_API_KEY`: Your LLM provider API key
- `BACKEND_HOST`: Host to bind to (default: 0.0.0.0)
- `BACKEND_PORT`: Port to bind to (default: 8000, but Hugging Face will set this automatically)
- `DATABASE_URL`: Database connection string (uses SQLite by default)
- `QDRANT_HOST`: Qdrant vector database host
- `QDRANT_PORT`: Qdrant vector database port

### Notes

- The backend will automatically initialize the database on startup
- Textbook content is loaded from the `docs` directory during startup
- The service will be available at `https://your-username.hf.space`

## Architecture

- Backend: FastAPI application with RAG functionality
- Database: SQLite for session data (can be configured for PostgreSQL)
- Vector Database: Qdrant for textbook content embeddings
- LLM: Groq API for response generation
- Authentication: JWT-based authentication system
- Translation: AI-powered Urdu translation capabilities

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