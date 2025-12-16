import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(src_dir))

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, CollectionConfig
from config import settings
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
                # Load actual textbook content from docs directory for demo purposes
                self.demo_content = self._load_demo_content()

            def _load_demo_content(self):
                """Load actual textbook content from MDX files"""
                import os
                import sys
                from pathlib import Path
                import markdown
                from bs4 import BeautifulSoup

                # Try multiple possible paths for docs directory
                current_dir = Path(__file__).parent.parent  # backend/src/

                # Try different relative paths
                possible_paths = [
                    current_dir / "docs",  # backend/src/docs (current)
                    current_dir.parent / "docs",  # backend/docs (parent of src)
                    current_dir.parent.parent / "docs",  # project root /docs (go up 2 from src)
                    Path("docs"),  # relative to current working directory
                    Path(__file__).parent.parent.parent / "docs",  # go up 3 to project root
                ]

                docs_path = None
                for path in possible_paths:
                    if path.exists():
                        docs_path = path
                        logger.info(f"Found docs directory at: {path}")
                        break

                if docs_path is None:
                    logger.warning("Could not find docs directory in any expected location")
                    return []

                demo_content = []
                content_id = 1

                if docs_path.exists():
                    # Find all MDX files in the docs directory
                    for mdx_file in docs_path.rglob("*.mdx"):
                        try:
                            with open(mdx_file, 'r', encoding='utf-8') as f:
                                content = f.read()

                            # Remove frontmatter if present
                            if content.startswith('---'):
                                parts = content.split('---', 2)
                                if len(parts) > 2:
                                    content = parts[2]

                            # Convert markdown to plain text
                            html = markdown.markdown(content)
                            soup = BeautifulSoup(html, 'html.parser')
                            text = soup.get_text()

                            # Clean up extra whitespace
                            text = ' '.join(text.split())

                            # Split content into chunks if it's too large
                            chunk_size = 1000
                            overlap = 100
                            start = 0

                            while start < len(text):
                                end = start + chunk_size
                                chunk = text[start:end].strip()

                                if chunk:  # Only add non-empty chunks
                                    demo_content.append({
                                        "id": content_id,
                                        "content": chunk,
                                        "source_document": str(mdx_file),
                                        "metadata": {
                                            "file_path": str(mdx_file),
                                            "chunk_size": len(chunk)
                                        }
                                    })
                                    content_id += 1

                                start = end - overlap if end < len(text) else end

                                # Stop if we have too many entries to avoid memory issues
                                if content_id > 100:  # Limit to 100 entries max
                                    break

                        except Exception as e:
                            logger.warning(f"Could not read MDX file {mdx_file}: {e}")
                            continue

                # If no MDX files were found, use default content
                if not demo_content:
                    logger.warning("No MDX files found, using default demo content")
                    demo_content = [
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

                logger.info(f"Loaded {len(demo_content)} content chunks for mock client")
                return demo_content

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