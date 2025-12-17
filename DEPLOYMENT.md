# Deployment Guide

This guide explains how to deploy the Physical AI Humanoid Robotics Textbook project to Vercel (frontend) and Hugging Face Spaces (backend).

## Architecture Overview

The project consists of two separate services:
1. **Frontend**: A Docusaurus-based documentation site deployed on Vercel
2. **Backend**: A FastAPI RAG service deployed on Hugging Face Spaces

The frontend connects to the backend via the `BACKEND_URL` environment variable.

## Backend Deployment (Hugging Face Spaces)

### Prerequisites
- Hugging Face account
- Groq API key (or other LLM provider API key)

### Steps
1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Choose "Cuda 12.1" or "Base image" as the hardware
4. Add your repository files to the Space
5. The `Dockerfile` and `app.py` in the root directory will be used automatically
6. Add your API keys as Space secrets:
   - `GROQ_API_KEY`: Your Groq API key
   - Or other required API keys

### Configuration
The backend uses environment variables from the `.env` file:
- `GROQ_API_KEY`: Your LLM provider API key
- `BACKEND_HOST`: Host to bind to (default: 0.0.0.0)
- `BACKEND_PORT`: Port to bind to (default: 8000)
- `DATABASE_URL`: Database connection string (uses SQLite by default)
- `QDRANT_HOST`: Qdrant vector database host
- `QDRANT_PORT`: Qdrant vector database port

### Notes
- The backend will automatically initialize the database on startup
- Textbook content is loaded from the `docs` directory during startup
- The service will be available at `https://your-username.hf.space`

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account
- Deployed backend service

### Steps
1. Push your code to a GitHub repository
2. Go to [Vercel](https://vercel.com) and sign in
3. Click "New Project" and import your GitHub repository
4. Configure the project settings:
   - Framework Preset: `Docusaurus`
   - Root Directory: `.` (root)
5. Add environment variables in the Vercel dashboard:
   - `BACKEND_URL`: The URL of your deployed backend (e.g., `https://your-backend-app.hf.space`)
6. Click "Deploy"

### Configuration
- The frontend will automatically connect to the backend API
- CORS headers are configured in `vercel.json`
- No additional configuration needed beyond the `BACKEND_URL` environment variable

## Connecting Frontend and Backend

Once both services are deployed:

1. The backend will be available at `https://your-username.hf.space`
2. Set this URL as the `BACKEND_URL` environment variable in your Vercel project
3. Redeploy the frontend if needed
4. The frontend will now connect to the deployed backend

## Environment Variables

### Backend (Hugging Face Spaces - as Secrets)
- `GROQ_API_KEY`: Your LLM provider API key
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)
- Other variables can be configured in the Dockerfile if needed

### Frontend (Vercel Environment Variables)
- `BACKEND_URL`: URL of the deployed backend service (e.g., `https://your-backend.hf.space`)

## Troubleshooting

### Frontend Issues
- If the chatbot doesn't work, check that `BACKEND_URL` is set correctly in Vercel
- Verify that the backend service is running and accessible
- Check browser console for API errors

### Backend Issues
- Ensure all required environment variables (API keys) are set as Space secrets
- Check the Hugging Face Space logs for errors
- Verify that the database initialized correctly

### CORS Issues
- The `vercel.json` file includes CORS headers to handle cross-origin requests
- If issues persist, ensure the backend allows requests from your frontend domain

## Scaling Considerations

### Backend
- For production use, consider using PostgreSQL instead of SQLite
- Consider using a dedicated Qdrant instance instead of the local one
- Monitor API usage for your LLM provider

### Frontend
- Vercel provides global CDN and auto-scaling
- The chatbot widget is optimized for performance
- Static content is served efficiently through Vercel's CDN