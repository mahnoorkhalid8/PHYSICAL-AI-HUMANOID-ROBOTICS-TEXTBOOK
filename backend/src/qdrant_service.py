from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, CollectionConfig
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Global client instance (initialized lazily)
_qdrant_client = None

def get_qdrant_client():
    """
    Creates and returns a Qdrant client instance based on configuration.
    The client is created lazily to avoid startup failures when Qdrant is not available.
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

        _qdrant_client = client
        return client
    except Exception as e:
        logger.warning(f"Could not connect to Qdrant at {settings.qdrant_host}:{settings.qdrant_port}. Error: {e}")
        logger.warning("Qdrant service will be unavailable until connection is established.")
        # Return a mock client that simulates Qdrant functionality for demo purposes
        class MockQdrantClient:
            def __init__(self):
                # Sample textbook content for demo purposes
                self.demo_content = [
                    {
                        "id": 1,
                        "content": "Physical AI is an approach that integrates artificial intelligence with physical systems, focusing on embodied intelligence where AI learns through interaction with the real world. This approach emphasizes the importance of physics, embodiment, and real-world interaction in developing intelligent systems.",
                        "source_document": "../docs/intro.mdx",
                        "metadata": {"file_path": "../docs/intro.mdx", "chunk_size": 100}
                    },
                    {
                        "id": 2,
                        "content": "Humanoid robotics combines principles from robotics, biomechanics, and cognitive science to create robots with human-like form and capabilities. These robots are designed to interact with human environments and perform tasks in ways similar to humans.",
                        "source_document": "../docs/humanoid-robotics.mdx",
                        "metadata": {"file_path": "../docs/humanoid-robotics.mdx", "chunk_size": 100}
                    },
                    {
                        "id": 3,
                        "content": "The robotic nervous system refers to the control architecture that enables humanoid robots to perceive, process, and respond to their environment. It includes sensors, actuators, and control algorithms that work together to achieve coordinated movement and behavior.",
                        "source_document": "../docs/robotic-nervous-system.mdx",
                        "metadata": {"file_path": "../docs/robotic-nervous-system.mdx", "chunk_size": 100}
                    },
                    {
                        "id": 4,
                        "content": "Control systems in humanoid robotics involve complex algorithms for balance, locomotion, and manipulation. These systems must handle real-time processing, adapt to changing environments, and ensure stable and safe operation of the robot.",
                        "source_document": "../docs/control-systems.mdx",
                        "metadata": {"file_path": "../docs/control-systems.mdx", "chunk_size": 100}
                    }
                ]

            def search(self, collection_name, query_vector, limit, with_payload):
                # For the mock client, we'll return all demo content
                # The actual filtering will be done in rag_service based on the text query
                return self.demo_content[:limit]

            def get_collection(self, collection_name):
                # Simulate collection exists
                return {"status": "collection_exists"}

            def upsert(self, collection_name, points):
                # Simulate storing data
                print(f"Simulated upsert to collection {collection_name} with {len(points)} points")

        _qdrant_client = MockQdrantClient()
        return _qdrant_client