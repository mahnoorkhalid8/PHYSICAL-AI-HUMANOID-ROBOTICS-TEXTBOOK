import os
import sys
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import models
from groq import Groq

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(src_dir))

from qdrant_service import get_qdrant_client
from config import settings
import logging
import markdown
from bs4 import BeautifulSoup
import uuid

logger = logging.getLogger(__name__)

class BookIngestor:
    def __init__(self):
        # Initialize the Groq client (though we're using mock embeddings for now)
        # Note: Groq doesn't provide embedding services, so we'll continue using mock embeddings
        self.collection_name = settings.qdrant_collection_name

    def extract_text_from_mdx(self, file_path: str) -> str:
        """Extract text content from MDX file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove frontmatter if present (content between ---)
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

        return text

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # If this isn't the last chunk, try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings near the chunk boundary
                snippet = text[start:end + 200]  # Look ahead a bit
                sentence_endings = [snippet.rfind('.', start, end),
                                  snippet.rfind('!', start, end),
                                  snippet.rfind('?', start, end)]
                best_ending = max(sentence_endings)

                if best_ending > start + chunk_size // 2:  # Only if it's not too close to start
                    end = best_ending + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - overlap if end < len(text) else end

        return chunks

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text - using mock embeddings since Gemini doesn't provide direct embeddings"""
        # Note: Google's embedding API is separate from Gemini, so for now we'll use mock embeddings
        # For production use, you would want to use Google's dedicated embedding API
        # Generate a consistent mock embedding based on text hash
        import numpy as np
        text_hash = hash(text) % (2**32)
        np.random.seed(text_hash)
        mock_embedding = np.random.random(1536).tolist()  # Standard embedding size
        return mock_embedding

    async def process_book_directory(self, directory_path: str):
        """Process all MDX files in a directory and ingest into QDRANT"""
        directory = Path(directory_path)

        if not directory.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return

        mdx_files = list(directory.rglob("*.mdx"))
        logger.info(f"Found {len(mdx_files)} MDX files to process")

        points = []
        point_id = 0

        for mdx_file in mdx_files:
            logger.info(f"Processing file: {mdx_file}")

            try:
                # Extract text from MDX file
                text_content = self.extract_text_from_mdx(str(mdx_file))

                # Chunk the text
                chunks = self.chunk_text(text_content)

                for i, chunk in enumerate(chunks):
                    if len(chunk) < 20:  # Skip very small chunks
                        continue

                    # Get embedding for the chunk
                    embedding = self.get_embedding(chunk)

                    # Create a Qdrant point
                    point = models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "content": chunk,
                            "source_document": str(mdx_file),
                            "chunk_index": i,
                            "content_type": "text",
                            "metadata": {
                                "file_path": str(mdx_file),
                                "chunk_size": len(chunk)
                            }
                        }
                    )

                    points.append(point)
                    point_id += 1

                    # Batch insert every 100 points to avoid memory issues
                    if len(points) >= 100:
                        self._insert_batch(points)
                        points = []

            except Exception as e:
                logger.error(f"Error processing file {mdx_file}: {str(e)}")
                continue

        # Insert remaining points
        if points:
            self._insert_batch(points)

        logger.info(f"Ingestion completed. Total points added: {point_id}")

    def _insert_batch(self, points: List[models.PointStruct]):
        """Insert a batch of points into Qdrant"""
        try:
            get_qdrant_client().upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Inserted {len(points)} points into collection {self.collection_name}")
        except Exception as e:
            logger.error(f"Error inserting batch: {str(e)}")
            raise

async def main():
    """Main function to run the ingestion process"""
    ingestor = BookIngestor()

    # Path to the book content - adjust as needed
    book_path = "../../docs"  # Relative to backend/src/ (going up two levels to project root, then to docs)

    logger.info("Starting book ingestion process...")
    await ingestor.process_book_directory(book_path)
    logger.info("Book ingestion process completed!")

if __name__ == "__main__":
    asyncio.run(main())