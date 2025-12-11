from typing import List, Dict, Any, Optional
from groq import Groq
from ..qdrant_service import get_qdrant_client
from ..models.vector_embedding import SearchQuery, VectorEmbedding
from ..config import settings
from ..logging_config import logger
import uuid
import numpy as np

class RAGService:
    def __init__(self):
        # Initialize the Groq client
        self.client = Groq(api_key=settings.groq_api_key)
        self.model_name = settings.groq_model
        self.collection_name = settings.qdrant_collection_name

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
                # For current page, prioritize results from the same document as the selected text
                # For now, we'll still combine the query and selected text, but in the future
                # we could add filters to limit to specific documents
                search_text = f"{query_text} Context: {selected_text}"
                query_embedding = self.get_query_embedding(search_text)

            # Search in Qdrant
            qdrant_client = get_qdrant_client()

            # For mock client compatibility, pass the query text as well
            # In a real implementation, the search would be based on vector similarity
            if hasattr(qdrant_client, 'demo_content'):
                # This is our mock client - perform keyword-based search using the original query
                search_results = []
                query_lower = query_text.lower()

                for item in qdrant_client.demo_content:
                    content_lower = item["content"].lower()
                    # Simple keyword matching for demo
                    if ("physical ai" in query_lower and "physical ai" in content_lower) or \
                       ("humanoid" in query_lower and "humanoid" in content_lower) or \
                       ("robotic" in query_lower and "robotic" in content_lower) or \
                       ("control" in query_lower and "control" in content_lower) or \
                       ("nervous system" in query_lower and "nervous system" in content_lower) or \
                       ("embodiment" in query_lower and "embodiment" in content_lower):
                        search_results.append(item)

                # If no keyword matches, return all demo content as fallback
                if not search_results:
                    search_results = qdrant_client.demo_content[:top_k]
                else:
                    search_results = search_results[:top_k]
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
                # Check if result is from mock client (dict) or real Qdrant (object with attributes)
                if isinstance(result, dict):
                    # This is a mock result
                    point_id = result.get("id", hash(str(result.get("content", ""))) % (2**31))
                    content = result.get("content", "")
                    source_document = result.get("source_document", "")
                    metadata = result.get("metadata", {})
                    score = result.get("score", 0.0)
                else:
                    # This is a real Qdrant result
                    # Handle potential ID type mismatch - convert to int if possible, otherwise use hash
                    try:
                        # Try to convert to int first
                        point_id = int(result.id) if isinstance(result.id, (int, str, float)) else hash(str(result.id)) % (2**31)
                    except (ValueError, TypeError):
                        # If conversion fails, use a hash-based integer
                        point_id = hash(str(result.id)) % (2**31)

                    content = result.payload.get("content", "") if hasattr(result, 'payload') else ""
                    source_document = result.payload.get("source_document", "") if hasattr(result, 'payload') else ""
                    metadata = result.payload.get("metadata", {}) if hasattr(result, 'payload') else {}
                    score = getattr(result, 'score', 0.0)

                vector_embedding = VectorEmbedding(
                    id=point_id,
                    content=content,
                    embedding_vector=[],  # We don't need the full embedding vector for the response
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
            # Return empty list instead of raising an exception to allow fallback response
            logger.warning("Returning empty context due to search error")
            return []

    def get_query_embedding(self, text: str) -> List[float]:
        """Get embedding for query text - using mock embeddings for now since we're using Gemini"""
        # Note: Google's embedding API is separate from Gemini, so for now we'll use mock embeddings
        # In a production system, you might want to use Google's dedicated embedding API
        try:
            # Generate a consistent mock embedding based on text hash
            text_hash = hash(text) % (2**32)
            np.random.seed(text_hash)
            mock_embedding = np.random.random(1536).tolist()  # Standard embedding size
            return mock_embedding
        except Exception as e:
            logger.error(f"Error getting query embedding: {str(e)}")
            # Return a fallback embedding
            return np.random.random(1536).tolist()

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
            # Check if the error is related to API key issues
            error_str = str(e).lower()
            if "api" in error_str and ("key" in error_str or "auth" in error_str or "invalid" in error_str or "401" in error_str or "403" in error_str):
                return f"I'm sorry, but there's an issue with the API key. The API returned an authentication error. Please verify your API key in the .env file is correct and active. Error details: {str(e)}"
            elif "400" in error_str:
                return f"I'm sorry, there's an issue with the API request. The API returned a 400 error, which might be due to the model name or request format. Current model: {self.model_name}. Error details: {str(e)}"
            elif "429" in error_str:
                return f"I'm sorry, you've exceeded the API rate limit or quota. Please check your API plan and usage. Error details: {str(e)}"
            else:
                # For other errors, provide more helpful fallback
                if len(context_list) > 0:
                    # If we have context but can't generate an answer, provide a summary of the context
                    context_preview = context_list[0].content[:200] + "..." if len(context_list[0].content) > 200 else context_list[0].content
                    return f"I found some relevant information in the textbook: '{context_preview}'. However, I encountered an error calling the API. Error: {str(e)}"
                else:
                    # No context and API error - provide guidance
                    return f"I'm sorry, I couldn't find relevant information in the textbook and encountered an API error. Error: {str(e)}"

    def process_query(self, query: str, selected_text: Optional[str] = None, search_scope: str = "full_book") -> Dict[str, Any]:
        """
        Process a RAG query end-to-end: search, generate answer, format response
        """
        try:
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
                "timestamp": "2025-12-10T10:30:00Z"  # In real implementation, use actual timestamp
            }

            logger.info(f"Successfully processed query: {query[:50]}... (scope: {search_scope})")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise