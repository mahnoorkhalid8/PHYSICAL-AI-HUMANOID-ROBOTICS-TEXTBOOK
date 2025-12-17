import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_selected_text_context_query_integration():
    """Integration test for selected-text RAG query"""

    # Mock the Qdrant search response
    mock_search_result = [
        MagicMock(
            payload={
                "content": "The ROS2 architecture provides a flexible framework for writing robot software. It includes nodes, topics, and services for communication.",
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
            mock_completion.choices = [Mock(message=Mock(content="The ROS2 architecture provides a flexible framework for writing robot software with nodes, topics, and services for communication."))]
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

            # Verify sources are returned
            assert len(data["sources"]) > 0
            assert data["sources"][0]["title"] is not None
            assert data["sources"][0]["url"] is not None

def test_current_page_context_query_integration():
    """Integration test for current-page RAG query"""

    # Mock the Qdrant search response
    mock_search_result = [
        MagicMock(
            payload={
                "content": "ROS2 Nodes are processes that perform computation. They are the fundamental building blocks of a ROS system.",
                "source_document": "/docs/01-robotic-nervous-system/ros2-nodes-topics-services.mdx",
                "chunk_index": 0
            },
            score=0.92
        )
    ]

    with patch('backend.src.qdrant_client.qdrant_client') as mock_qdrant:
        mock_qdrant.search.return_value = mock_search_result

        # Mock the OpenAI client
        with patch('backend.src.services.rag_service.OpenAI') as mock_openai_class:
            mock_openai_instance = Mock()
            mock_completion = Mock()
            mock_completion.choices = [Mock(message=Mock(content="ROS2 Nodes are processes that perform computation and are the fundamental building blocks of a ROS system."))]
            mock_openai_instance.chat.completions.create.return_value = mock_completion
            mock_openai_class.return_value = mock_openai_instance

            payload = {
                "question": "What are ROS2 Nodes?",
                "selected_text": "ROS2 Nodes are processes that perform computation.",
                "context": {
                    "search_scope": "current_page"
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

def test_context_aware_query_with_no_selected_text():
    """Test that queries without selected_text still work with appropriate context"""

    # Mock the Qdrant search response
    mock_search_result = [
        MagicMock(
            payload={
                "content": "ROS2 is a flexible framework for robotics applications.",
                "source_document": "/docs/01-robotic-nervous-system/ros2-architecture.mdx",
                "chunk_index": 0
            },
            score=0.88
        )
    ]

    with patch('backend.src.qdrant_client.qdrant_client') as mock_qdrant:
        mock_qdrant.search.return_value = mock_search_result

        # Mock the OpenAI client
        with patch('backend.src.services.rag_service.OpenAI') as mock_openai_class:
            mock_openai_instance = Mock()
            mock_completion = Mock()
            mock_completion.choices = [Mock(message=Mock(content="ROS2 is a flexible framework for robotics applications."))]
            mock_openai_instance.chat.completions.create.return_value = mock_completion
            mock_openai_class.return_value = mock_openai_instance

            payload = {
                "question": "What is ROS2?",
                "context": {
                    "search_scope": "full_book"
                }
            }

            response = client.post("/api/query", json=payload)

            # Should still return successful response
            assert response.status_code == 200
            data = response.json()

            # Verify response structure
            assert "answer" in data
            assert "sources" in data
            assert "query_id" in data
            assert "timestamp" in data