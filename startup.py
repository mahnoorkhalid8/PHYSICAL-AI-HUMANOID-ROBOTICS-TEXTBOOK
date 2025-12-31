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
    max_retries = 30  # 30 * 2 seconds = 60 seconds max wait
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Create Qdrant client with proper configuration
            if settings.cluster_endpoint:
                # Using Qdrant cloud
                client = QdrantClient(
                    url=settings.cluster_endpoint,
                    api_key=settings.qdrant_api_key
                )
            else:
                # Using local Qdrant
                client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port,
                    api_key=settings.qdrant_api_key
                )

            # Test connection
            client.get_collections()
            logger.info("Qdrant is available!")
            return True
        except Exception as e:
            logger.info(f"Waiting for Qdrant... (attempt {retry_count + 1}) Error: {e}")
            time.sleep(2)
            retry_count += 1

    logger.error("Qdrant never became available!")
    return False

def ensure_data_ingested():
    """Ensure that textbook data is ingested into the vector database"""
    try:
        # Check if collection exists and has data
        from backend.src.qdrant_service import qdrant_client

        try:
            collection_info = qdrant_client.get_collection(settings.qdrant_collection_name)
            logger.info(f"Collection {settings.qdrant_collection_name} exists with {collection_info.points_count} points")

            if collection_info.points_count == 0:
                logger.info("No points in collection, starting ingestion...")
                # Run ingestion
                import asyncio
                ingestor = BookIngestor()
                asyncio.run(ingestor.process_book_directory("../docs"))  # Relative to backend/src/
            else:
                logger.info("Collection already has data, skipping ingestion")
        except Exception as e:
            logger.info(f"Collection doesn't exist, creating and ingesting data: {e}")
            # Run ingestion
            import asyncio
            ingestor = BookIngestor()
            asyncio.run(ingestor.process_book_directory("../docs"))  # Relative to backend/src/

    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
        raise

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

    # Initialize database first
    initialize_database()

    # Wait for Qdrant to be available
    if not wait_for_qdrant():
        logger.error("Failed to connect to Qdrant, exiting...")
        exit(1)

    # Ensure data is ingested
    ensure_data_ingested()

    logger.info("Startup initialization completed successfully!")