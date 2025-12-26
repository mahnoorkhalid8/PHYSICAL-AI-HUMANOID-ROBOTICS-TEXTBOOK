from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.personalize import router as personalize_router
from src.api.query_endpoint import router as query_router
from src.api.session_endpoint import router as session_router

# Create FastAPI app instance
app = FastAPI(
    title="AI Textbook Backend API",
    description="Backend API for AI-powered textbook features including chatbot and personalization",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the personalization API router
app.include_router(
    personalize_router,
    prefix="/api",
    tags=["personalization"]
)

# Include the chatbot query API router
app.include_router(
    query_router,
    prefix="/api",
    tags=["query"]
)

# Include the chatbot session API router
app.include_router(
    session_router,
    prefix="/api",
    tags=["session"]
)

@app.get("/")
def read_root():
    return {"message": "AI Textbook Backend API is running! Includes chatbot and personalization features."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/health")
def api_health_check():
    """Health check for all API endpoints"""
    return {
        "status": "healthy",
        "services": {
            "personalization": "available",
            "chatbot_query": "available",
            "chatbot_session": "available"
        }
    }