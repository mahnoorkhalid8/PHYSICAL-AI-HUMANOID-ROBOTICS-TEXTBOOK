from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, CollectionConfig
from .config import settings
import logging

logger = logging.getLogger(__name__)

def get_qdrant_client():
    """
    Creates and returns a Qdrant client instance based on configuration
    """
    if settings.cluster_endpoint:
        # Using cloud instance
        client = QdrantClient(
            url=settings.cluster_endpoint,
            api_key=settings.qdrant_api_key,
            https=True
        )
    else:
        # Using local instance
        client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )

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

    return client

# Create a global client instance
qdrant_client = get_qdrant_client()