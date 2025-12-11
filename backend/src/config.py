from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Backend Configuration
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))

    # Qdrant Configuration
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "book_embeddings")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    cluster_endpoint: Optional[str] = os.getenv("CLUSTER_ENDPOINT")

    # Postgres Configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/chatbot_db")

    # Groq Configuration
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama3-70b-8192")

    # Application Settings
    cors_origins: List[str] = eval(os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:3001", "https://yourdomain.com"]'))

    class Config:
        env_file = ".env"

settings = Settings()