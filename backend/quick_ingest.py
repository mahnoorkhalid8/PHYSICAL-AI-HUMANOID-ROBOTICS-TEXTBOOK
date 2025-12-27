#!/usr/bin/env python3
"""
Quick ingestion script to add book content to Qdrant with better error handling
"""
import os
import sys
import asyncio
from pathlib import Path
import logging
import time

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ingest import BookIngestor
from src.qdrant_service import qdrant_client
from src.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def quick_ingest():
    """Run a quick ingestion with smaller batches and error handling"""
    ingestor = BookIngestor()

    # Use the docs directory relative to the project root
    book_path = os.path.join(os.path.dirname(__file__), '..', 'docs')
    book_path = os.path.abspath(book_path)

    if not os.path.exists(book_path):
        logger.error(f"Book path does not exist: {book_path}")
        return

    logger.info(f"Starting ingestion from: {book_path}")

    # Count total files first
    mdx_files = list(Path(book_path).rglob("*.mdx"))
    logger.info(f"Found {len(mdx_files)} MDX files to process")

    total_points = 0
    points = []
    point_id = 0

    for i, mdx_file in enumerate(mdx_files):
        logger.info(f"Processing file {i+1}/{len(mdx_files)}: {mdx_file}")

        try:
            # Extract text from MDX file
            text_content = ingestor.extract_text_from_mdx(str(mdx_file))

            # Chunk the text
            chunks = ingestor.chunk_text(text_content, chunk_size=500, overlap=50)  # Smaller chunks

            for j, chunk in enumerate(chunks):
                if len(chunk) < 20:  # Skip very small chunks
                    continue

                # Get embedding for the chunk
                embedding = ingestor.get_embedding(chunk)

                # Create a Qdrant point
                point = {
                    "id": point_id,
                    "vector": embedding,
                    "payload": {
                        "content": chunk,
                        "source_document": str(mdx_file),
                        "chunk_index": j,
                        "content_type": "text",
                        "metadata": {
                            "file_path": str(mdx_file),
                            "chunk_size": len(chunk)
                        }
                    }
                }

                points.append(point)
                point_id += 1
                total_points += 1

                # Insert smaller batches to avoid timeouts
                if len(points) >= 10:  # Much smaller batch size
                    try:
                        logger.info(f"Inserting batch of {len(points)} points...")
                        qdrant_client.upsert(
                            collection_name=settings.qdrant_collection_name,
                            points=points
                        )
                        logger.info(f"Successfully inserted {len(points)} points")
                        points = []  # Clear the batch
                    except Exception as e:
                        logger.error(f"Error inserting batch: {str(e)}")
                        logger.info("Retrying with even smaller batch...")
                        # If batch fails, try inserting one by one
                        for point in points:
                            try:
                                qdrant_client.upsert(
                                    collection_name=settings.qdrant_collection_name,
                                    points=[point]
                                )
                            except Exception as e2:
                                logger.error(f"Failed to insert single point {point['id']}: {str(e2)}")
                        points = []  # Clear the batch after handling errors

        except Exception as e:
            logger.error(f"Error processing file {mdx_file}: {str(e)}")
            continue

    # Insert any remaining points
    if points:
        try:
            logger.info(f"Inserting final batch of {len(points)} points...")
            qdrant_client.upsert(
                collection_name=settings.qdrant_collection_name,
                points=points
            )
            logger.info(f"Successfully inserted final {len(points)} points")
        except Exception as e:
            logger.error(f"Error inserting final batch: {str(e)}")

    logger.info(f"Ingestion completed. Total points processed: {total_points}")

if __name__ == "__main__":
    asyncio.run(quick_ingest())