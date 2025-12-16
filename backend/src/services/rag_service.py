import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(src_dir))

from typing import List, Dict, Any, Optional
from groq import Groq
from qdrant_service import get_qdrant_client
from models.vector_embedding import SearchQuery, VectorEmbedding
from config import settings
from logging_config import logger
import uuid
import numpy as np
import traceback
from sentence_transformers import SentenceTransformer

class RAGService:
    def __init__(self):
        # Initialize the Groq client
        if not settings.groq_api_key:
            logger.warning("GROQ_API_KEY not found in environment variables. RAG service will fail on generation.")
        
        self.client = Groq(api_key=settings.groq_api_key)
        self.model_name = settings.groq_model
        self.collection_name = settings.qdrant_collection_name
        
        # Initialize embedding model (using a lightweight local model)
        try:
            logger.info("Loading embedding model: all-MiniLM-L6-v2...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.embedding_model = None

    def search_embeddings(self, query_text: str, top_k: int = 5, selected_text: Optional[str] = None, search_scope: str = "full_book") -> List[VectorEmbedding]:
        """
        Search for relevant embeddings in Qdrant based on the query and search scope
        """
        try:
            # Get embedding for the query text
            query_embedding = self.get_query_embedding(query_text)

            # Modify the search based on the search scope
            search_text = query_text
            if search_scope == "selected_text" and selected_text:
                # When searching in selected text context, combine query and selected text
                search_text = f"{query_text} Context: {selected_text}"
                query_embedding = self.get_query_embedding(search_text)
            elif search_scope == "current_page" and selected_text:
                search_text = f"{query_text} Context: {selected_text}"
                query_embedding = self.get_query_embedding(search_text)

            # Search in Qdrant
            qdrant_client = get_qdrant_client()

            # For mock client compatibility, pass the query text as well
            if hasattr(qdrant_client, 'demo_content'):
                # This is a mock client - perform better search on all content
                query_lower = query_text.lower()

                # Calculate similarity scores for all content
                scored_results = []
                for item in qdrant_client.demo_content:
                    content_lower = item["content"].lower()

                    # Calculate a simple similarity score based on keyword matches
                    query_words = set(query_lower.split())
                    content_words = set(content_lower.split())

                    # Count matching words
                    matches = len(query_words.intersection(content_words))

                    # Calculate similarity score (higher for more matches)
                    similarity_score = matches / len(query_words) if query_words else 0

                    # Also consider word overlap percentage
                    if content_words:
                        overlap_score = matches / len(content_words)
                        final_score = (similarity_score + overlap_score) / 2
                    else:
                        final_score = 0

                    # Add some bonus for exact phrase matches
                    if query_lower in content_lower:
                        final_score += 0.5  # Bonus for exact phrase match

                    scored_results.append((item, final_score))

                # Sort by score in descending order
                scored_results.sort(key=lambda x: x[1], reverse=True)

                # Take top_k results with their scores
                search_results = []
                for item, score in scored_results[:top_k]:
                    # Add the score to the item
                    item_with_score = item.copy()
                    item_with_score['score'] = score
                    search_results.append(item_with_score)
            else:
                # This is a real Qdrant client
                search_results = qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embedding,
                    limit=top_k,
                    with_payload=True
                )

            # Convert results to VectorEmbedding objects
            vector_embeddings = []
            for result in search_results:
                if isinstance(result, dict):
                    point_id = result.get("id", hash(str(result.get("content", ""))) % (2**31))
                    content = result.get("content", "")
                    source_document = result.get("source_document", "")
                    metadata = result.get("metadata", {})
                    score = result.get("score", 0.0)
                else:
                    try:
                        point_id = int(result.id) if isinstance(result.id, (int, str, float)) else hash(str(result.id)) % (2**31)
                    except (ValueError, TypeError):
                        point_id = hash(str(result.id)) % (2**31)

                    content = result.payload.get("content", "") if hasattr(result, 'payload') else ""
                    source_document = result.payload.get("source_document", "") if hasattr(result, 'payload') else ""
                    metadata = result.payload.get("metadata", {}) if hasattr(result, 'payload') else {}
                    score = getattr(result, 'score', 0.0)

                vector_embedding = VectorEmbedding(
                    id=point_id,
                    content=content,
                    embedding_vector=[], 
                    content_type="text",
                    source_document=source_document,
                    metadata=metadata,
                    score=score
                )
                vector_embeddings.append(vector_embedding)

            logger.info(f"Found {len(vector_embeddings)} relevant results for query: {query_text[:50]}... (scope: {search_scope})")
            return vector_embeddings

        except Exception as e:
            logger.error(f"Error searching embeddings: {str(e)}")
            logger.error(traceback.format_exc())
            # Do NOT swallow the error here unless we really want 0 results. 
            # Re-raising allows the endpoint to return a 500 error which is cleaner for debugging.
            raise e 

    def get_query_embedding(self, text: str) -> List[float]:
        """Get embedding for query text using SentenceTransformer"""
        try:
            if self.embedding_model:
                # Generate embedding
                embedding = self.embedding_model.encode(text).tolist()
                return embedding
            else:
                logger.warning("Embedding model not loaded. Using fallback random embedding.")
                # Fallback to random if model failed to load (preserves old behavior just in case)
                text_hash = hash(text) % (2**32)
                np.random.seed(text_hash)
                return np.random.random(384).tolist() # Match MiniLM dimension
        except Exception as e:
            logger.error(f"Error getting query embedding: {str(e)}")
            return np.random.random(384).tolist()

    def generate_answer(self, query: str, context_list: List[VectorEmbedding], selected_text: Optional[str] = None, search_scope: str = "full_book") -> str:
        """
        Generate an answer using Groq based on the query and retrieved context
        """
        try:
            # Combine the context information
            context_str = ""
            for i, ctx in enumerate(context_list):
                context_str += f"Source {i+1}: {ctx.content}\n\n"

            # Prepare the prompt for Groq based on search scope
            if search_scope == "selected_text" and selected_text:
                system_prompt = f"""You are an AI assistant helping students understand the Physical AI Humanoid Robotics textbook. Provide clear, accurate answers based on the textbook content and the selected text context. Focus your answer on explaining or elaborating on the selected text. If the information is not available in the provided context, please say so clearly."""

                user_prompt = f"""
                The user has selected the following text: "{selected_text}"

                The user's question is: "{query}"

                Here is relevant context from the textbook:
                {context_str}
                """
            elif search_scope == "current_page" and selected_text:
                system_prompt = f"""You are an AI assistant helping students understand the Physical AI Humanoid Robotics textbook. Provide clear, accurate answers based on the textbook content. Consider that the user is looking at content related to the selected text. If the information is not available in the provided context, please say so clearly."""

                user_prompt = f"""
                The user is currently viewing content that includes: "{selected_text}"

                The user's question is: "{query}"

                Here is relevant context from the textbook:
                {context_str}
                """
            else:  # full_book
                system_prompt = f"""You are an AI assistant helping students understand the Physical AI Humanoid Robotics textbook. Provide clear, accurate answers based on the textbook content. If the information is not available in the provided context, please say so clearly."""

                user_prompt = f"""
                The user's question is: "{query}"

                Here is relevant context from the textbook:
                {context_str}
                """

            if not self.client.api_key:
                 raise ValueError("GROQ_API_KEY is missing. Cannot generate answer.")

            # Call Groq API to generate the answer
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.3,
                max_tokens=1000,
            )

            answer = chat_completion.choices[0].message.content
            logger.info(f"Generated answer for query: {query[:50]}... (scope: {search_scope})")
            return answer

        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Check if the error is related to API key issues
            error_str = str(e).lower()
            if "api" in error_str and ("key" in error_str or "auth" in error_str or "invalid" in error_str or "401" in error_str or "403" in error_str):
                raise ValueError(f"API Key Error: {str(e)}")
            
            # Re-raise to be handled by the endpoint for now, or fallback if critical
            # Raising lets the endpoint return a 500 with details which is better for debugging
            raise e

    def process_query(self, query: str, selected_text: Optional[str] = None, search_scope: str = "full_book") -> Dict[str, Any]:
        """
        Process a RAG query end-to-end: search, generate answer, format response
        """
        # Note: No try-except here, we want exceptions to bubble up to the endpoint
        
        # Search for relevant context
        context_list = self.search_embeddings(query, top_k=5, selected_text=selected_text, search_scope=search_scope)

        # Generate answer based on context
        answer = self.generate_answer(query, context_list, selected_text, search_scope)

        # Format sources for response
        sources = []
        for ctx in context_list:
            # Extract title from the source document path
            title = ctx.source_document.split('/')[-1].replace('.mdx', '').replace('_', ' ').title()

            sources.append({
                "title": title,
                "url": ctx.source_document.replace('../../../docs', '').replace('.mdx', ''),
                "relevance_score": ctx.score or 0.0
            })

        # Generate a unique query ID
        query_id = str(uuid.uuid4())

        result = {
            "answer": answer,
            "sources": sources,
            "query_id": query_id,
            "timestamp": "2025-12-10T10:30:00Z" # In real implementation, use actual timestamp
        }

        logger.info(f"Successfully processed query: {query[:50]}... (scope: {search_scope})")
        return result