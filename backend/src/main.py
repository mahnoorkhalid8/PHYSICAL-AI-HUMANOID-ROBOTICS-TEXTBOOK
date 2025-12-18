# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .config import settings
# from .api import query_endpoint
# from .api import session_endpoint
# from .logging_config import logger
# from .db import Base, engine
# from .models.chat_session import ChatSession
# from .models.message import Message
# from .models.query_context import QueryContext
# from .models.vector_embedding import VectorEmbedding
# from .services.chat_service import ChatService
# from .services.rag_service import RAGService
# from sqlalchemy import inspect

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Initialize database tables on startup
#     logger.info("Initializing database tables...")
#     try:
#         Base.metadata.create_all(bind=engine)
#         logger.info("Database tables created successfully!")

#         # Verify tables were created
#         inspector = inspect(engine)
#         tables = inspector.get_table_names()
#         logger.info(f"Available tables: {tables}")

#         # Pre-initialize services to avoid first-request delays
#         logger.info("Pre-initializing services...")
#         try:
#             # Try to create a RAG service to ensure Qdrant connection is established
#             rag_service = RAGService()
#             logger.info("RAG service initialized successfully")
#         except Exception as e:
#             logger.error(f"Error initializing RAG service: {e}")
#             # Don't raise exception here as we want the app to start anyway
#             # The error will be handled during actual requests

#         try:
#             # Try to create a chat service
#             chat_service = ChatService()
#             logger.info("Chat service initialized successfully")
#         except Exception as e:
#             logger.error(f"Error initializing Chat service: {e}")

#     except Exception as e:
#         logger.error(f"Error during startup initialization: {e}")
#         raise
#     yield
#     # Shutdown logic can go here if needed


# app = FastAPI(
#     title="RAG Chatbot API",
#     description="API for RAG-based textbook query system",
#     version="1.0.0",
#     lifespan=lifespan
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.cors_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API routes
# app.include_router(query_endpoint.router, prefix="/api", tags=["query"])
# app.include_router(session_endpoint.router, prefix="/api", tags=["session"])

# @app.get("/")
# def read_root():
#     return {"message": "RAG Chatbot API is running!"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import query_endpoint
from .api import session_endpoint
from .logging_config import logger
from .db import Base, engine
from .models.chat_session import ChatSession
from .models.message import Message
from .models.query_context import QueryContext
from .models.vector_embedding import VectorEmbedding
from sqlalchemy import inspect

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")

        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Available tables: {tables}")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    yield
    # Shutdown logic can go here if needed


app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based textbook query system",
    version="1.0.0",
    lifespan=lifespan
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