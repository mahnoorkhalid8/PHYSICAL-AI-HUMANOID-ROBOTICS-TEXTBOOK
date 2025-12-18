from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, CollectionConfig
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Global client instance, initialized lazily
_qdrant_client = None

def get_qdrant_client():
    """
    Creates and returns a Qdrant client instance based on configuration
    """
    global _qdrant_client

    if _qdrant_client is not None:
        return _qdrant_client

    try:
        if settings.cluster_endpoint:
            # Using cloud instance
            client = QdrantClient(
                url=settings.cluster_endpoint,
                api_key=settings.qdrant_api_key,
                https=True
            )
        else:
            # Using local instance - specify full URL for proper connection
            client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

        # Ensure the collection exists
        try:
            client.get_collection(settings.qdrant_collection_name)
            logger.info(f"Collection '{settings.qdrant_collection_name}' already exists")
        except:
            # Create collection if it doesn't exist
            client.create_collection(
                collection_name=settings.qdrant_collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # Assuming OpenAI embeddings
            )
            logger.info(f"Created collection '{settings.qdrant_collection_name}'")

        _qdrant_client = client
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")
        logger.error("Qdrant connection failed. Make sure Qdrant server is running and accessible.")
        # Re-raise the exception to fail fast instead of masking the issue
        raise e

# Direct client instance instead of LazyQdrantClient wrapper
try:
    qdrant_client = get_qdrant_client()
except Exception as e:
    logger.error(f"Failed to initialize Qdrant client at startup: {e}")
    # Still create a mock client as fallback, but log the error
    class MockQdrantClient:
        def __getattr__(self, name):
            def method(*args, **kwargs):
                raise Exception(f"Qdrant service is not available: {str(e)}. Please start Qdrant server or configure the connection properly.")
            return method
    qdrant_client = MockQdrantClient()