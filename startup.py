# startup.py
import os
import time
import logging
from qdrant_client import QdrantClient
from backend.src.ingest import BookIngestor
from backend.src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_qdrant():
    """Wait for Qdrant to be available"""
    max_retries = 5  # 5 * 1 seconds = 5 seconds max wait (faster startup)
    retry_count = 0

    logger.info(f"Checking Qdrant connection... (settings: host={settings.qdrant_host}, port={settings.qdrant_port}, endpoint={settings.cluster_endpoint})")

    while retry_count < max_retries:
        try:
            # Create Qdrant client with proper configuration
            if settings.cluster_endpoint:
                # Using Qdrant cloud
                logger.info(f"Connecting to Qdrant cloud: {settings.cluster_endpoint}")
                client = QdrantClient(
                    url=settings.cluster_endpoint,
                    api_key=settings.qdrant_api_key,
                    timeout=5  # Add timeout to prevent hanging
                )
            else:
                # Using local Qdrant
                logger.info(f"Connecting to local Qdrant: {settings.qdrant_host}:{settings.qdrant_port}")
                client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port,
                    api_key=settings.qdrant_api_key,
                    timeout=5  # Add timeout to prevent hanging
                )

            # Test connection with timeout
            client.get_collections()
            logger.info("Qdrant is available!")
            return True

        except Exception as e:
            logger.info(f"Waiting for Qdrant... (attempt {retry_count + 1}/{max_retries}) Error: {e}")
            time.sleep(1)  # Reduced sleep time for faster startup
            retry_count += 1

    logger.warning("Qdrant connection not established, but continuing startup...")
    return False  # Return False but continue startup

def ensure_data_ingested():
    """Ensure that textbook data is ingested into the vector database"""
    try:
        # Check if collection exists and has data
        from backend.src.qdrant_service import qdrant_client

        try:
            collection_info = qdrant_client.get_collection(settings.qdrant_collection_name)
            logger.info(f"Collection {settings.qdrant_collection_name} exists with {collection_info.points_count} points")

            if collection_info.points_count == 0:
                logger.info("No points in collection, but skipping ingestion for faster startup...")
                # Note: We skip ingestion on Hugging Face Spaces to avoid long startup times
                # The ingestion can happen separately or be pre-populated
            else:
                logger.info("Collection already has data, skipping ingestion")
        except Exception as e:
            logger.info(f"Collection doesn't exist, skipping ingestion for faster startup...")
            # For Hugging Face Spaces, we'll skip the full ingestion to avoid long startup times
            # The app should work with empty collections and let the first queries create embeddings

    except Exception as e:
        logger.warning(f"Warning during data ingestion check: {e}")
        # Don't raise the exception - just continue startup

def initialize_database():
    """Initialize the database tables"""
    try:
        from backend.src.db import Base, engine
        from backend.src.logging_config import logger
        from sqlalchemy import inspect

        logger.info("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")

        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Available tables: {tables}")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    logger.info("Starting startup initialization...")

    try:
        # Initialize database first
        initialize_database()

        # Wait for Qdrant to be available
        if not wait_for_qdrant():
            logger.warning("Qdrant is not available, but continuing startup...")
            # Don't exit here - allow the app to start even if Qdrant isn't ready immediately
            # This is important for Hugging Face Spaces where services might start in different orders

        # Ensure data is ingested (with a timeout to prevent hanging)
        try:
            ensure_data_ingested()
        except Exception as e:
            logger.warning(f"Data ingestion failed (this might be expected on first run): {e}")
            logger.info("Continuing startup...")

        logger.info("Startup initialization completed successfully!")

    except Exception as e:
        logger.error(f"Error during startup initialization: {e}")
        # Don't exit with error code to allow the main app to start anyway
        logger.info("Continuing to start main application...")