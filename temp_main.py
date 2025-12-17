from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import query_endpoint
from .api import session_endpoint
from .logging_config import logger

app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based textbook query system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(query_endpoint.router, prefix="/api", tags=["query"])
app.include_router(session_endpoint.router, prefix="/api", tags=["session"])

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}