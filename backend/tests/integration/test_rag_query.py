import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.qdrant_client import qdrant_client

client = TestClient(app)

def test_full_book_rag_query_integration():
    """Integration test for full-book RAG query"""

    # Mock the Qdrant search response
    mock_search_result = [
        MagicMock(
            payload={
                "content": "ROS2 (Robot Operating System 2) provides a flexible framework for writing robot software.",
                "source_document": "/docs/01-robotic-nervous-system/ros2-architecture.mdx",
                "chunk_index": 0
            },
            score=0.9
        )
    ]

    with patch('backend.src.qdrant_client.qdrant_client') as mock_qdrant:
        mock_qdrant.search.return_value = mock_search_result

        # Mock the OpenAI client
        with patch('backend.src.services.rag_service.OpenAI') as mock_openai_class:
            mock_openai_instance = Mock()
            mock_completion = Mock()
            mock_completion.choices = [Mock(message=Mock(content="ROS2 is a flexible framework for writing robot software."))]
            mock_openai_instance.chat.completions.create.return_value = mock_completion
            mock_openai_class.return_value = mock_openai_instance

            payload = {
                "question": "What is ROS2?",
                "context": {
                    "search_scope": "full_book"
                }
            }

            response = client.post("/api/query", json=payload)

            # Should return successful response
            assert response.status_code == 200
            data = response.json()

            # Verify response structure
            assert "answer" in data
            assert "sources" in data
            assert "query_id" in data
            assert "timestamp" in data

            # Verify answer was generated
            assert len(data["answer"]) > 0

            # Verify sources are returned
            assert len(data["sources"]) > 0
            assert data["sources"][0]["title"] is not None
            assert data["sources"][0]["url"] is not None

def test_selected_text_rag_query_integration():
    """Integration test for selected-text RAG query"""

    # Mock the Qdrant search response
    mock_search_result = [
        MagicMock(
            payload={
                "content": "The ROS2 architecture provides a flexible framework for writing robot software.",
                "source_document": "/docs/01-robotic-nervous-system/ros2-architecture.mdx",
                "chunk_index": 0
            },
            score=0.95
        )
    ]

    with patch('backend.src.qdrant_client.qdrant_client') as mock_qdrant:
        mock_qdrant.search.return_value = mock_search_result

        # Mock the OpenAI client
        with patch('backend.src.services.rag_service.OpenAI') as mock_openai_class:
            mock_openai_instance = Mock()
            mock_completion = Mock()
            mock_completion.choices = [Mock(message=Mock(content="The ROS2 architecture provides a flexible framework for writing robot software."))]
            mock_openai_instance.chat.completions.create.return_value = mock_completion
            mock_openai_class.return_value = mock_openai_instance

            payload = {
                "question": "Explain this architecture?",
                "selected_text": "The ROS2 architecture provides a flexible framework for writing robot software.",
                "context": {
                    "search_scope": "selected_text"
                }
            }

            response = client.post("/api/query", json=payload)

            # Should return successful response
            assert response.status_code == 200
            data = response.json()

            # Verify response structure
            assert "answer" in data
            assert "sources" in data
            assert "query_id" in data
            assert "timestamp" in data

            # Verify answer was generated
            assert len(data["answer"]) > 0

def test_rag_query_with_no_results():
    """Test RAG query when no relevant results are found"""

    # Mock empty search result
    mock_search_result = []

    with patch('backend.src.qdrant_client.qdrant_client') as mock_qdrant:
        mock_qdrant.search.return_value = mock_search_result

        # Mock the OpenAI client to handle the case where no context is provided
        with patch('backend.src.services.rag_service.OpenAI') as mock_openai_class:
            mock_openai_instance = Mock()
            mock_completion = Mock()
            mock_completion.choices = [Mock(message=Mock(content="I couldn't find relevant information in the textbook to answer your question."))]
            mock_openai_instance.chat.completions.create.return_value = mock_completion
            mock_openai_class.return_value = mock_openai_instance

            payload = {
                "question": "What is the meaning of life?",
                "context": {
                    "search_scope": "full_book"
                }
            }

            response = client.post("/api/query", json=payload)

            # Should still return successful response, but with appropriate answer
            assert response.status_code == 200
            data = response.json()

            # Verify response structure
            assert "answer" in data
            assert "sources" in data
            assert "query_id" in data
            assert "timestamp" in data

            # Sources should be empty if no results found
            assert len(data["sources"]) == 0