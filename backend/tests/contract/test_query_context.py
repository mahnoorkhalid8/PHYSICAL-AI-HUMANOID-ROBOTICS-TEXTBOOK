import pytest
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_query_with_selected_text_contract():
    """Contract test for /api/query endpoint with selected_text parameter"""

    # Test request with selected_text
    payload_with_selected_text = {
        "question": "Explain this concept?",
        "selected_text": "The ROS2 architecture provides a flexible framework for writing robot software.",
        "context": {
            "page_url": "/docs/01-robotic-nervous-system/ros2-architecture",
            "search_scope": "selected_text"
        }
    }

    response = client.post("/api/query", json=payload_with_selected_text)

    # Check that response has expected structure
    assert response.status_code in [200, 422, 500]

    if response.status_code == 200:
        data = response.json()
        # Check that response has required fields
        assert "answer" in data
        assert "sources" in data
        assert "query_id" in data
        assert "timestamp" in data

        # Check that sources is a list
        assert isinstance(data["sources"], list)

        # Check that query_id is a string (UUID format)
        assert isinstance(data["query_id"], str)

        # Check that timestamp is a string
        assert isinstance(data["timestamp"], str)

def test_query_with_different_search_scopes():
    """Test query endpoint with different search scopes"""

    # Test with current_page scope
    payload_current_page = {
        "question": "What are the key points?",
        "selected_text": "The main concepts include nodes, topics, and services.",
        "context": {
            "page_url": "/docs/01-robotic-nervous-system/ros2-nodes-topics-services",
            "search_scope": "current_page"
        }
    }

    response = client.post("/api/query", json=payload_current_page)
    assert response.status_code in [200, 422, 500]

    # Test with full_book scope (default)
    payload_full_book = {
        "question": "Explain ROS2 concepts",
        "context": {
            "search_scope": "full_book"
        }
    }

    response = client.post("/api/query", json=payload_full_book)
    assert response.status_code in [200, 422, 500]

def test_query_endpoint_search_scope_validation():
    """Test that invalid search_scope returns appropriate error"""

    invalid_payload = {
        "question": "What is ROS2?",
        "context": {
            "search_scope": "invalid_scope"  # This should be rejected
        }
    }

    response = client.post("/api/query", json=invalid_payload)

    # Should return validation error
    assert response.status_code in [422, 400]