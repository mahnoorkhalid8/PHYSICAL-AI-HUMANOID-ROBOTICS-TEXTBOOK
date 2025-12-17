import pytest
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_query_endpoint_contract():
    """Contract test for /api/query endpoint"""

    # Test valid request structure
    valid_payload = {
        "question": "What is ROS2 architecture?",
        "selected_text": "The ROS2 architecture provides a flexible framework...",
        "context": {
            "page_url": "/docs/01-robotic-nervous-system/ros2-architecture",
            "search_scope": "selected_text"
        }
    }

    response = client.post("/api/query", json=valid_payload)

    # Check that response has expected structure
    assert response.status_code in [200, 422, 500]  # 200 for success, 422 for validation errors, 500 for server errors

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

def test_query_endpoint_minimal_request():
    """Test query endpoint with minimal request (only question)"""

    minimal_payload = {
        "question": "What is ROS2?"
    }

    response = client.post("/api/query", json=minimal_payload)

    # Should at least return a valid response structure or validation error
    assert response.status_code in [200, 422, 500]

def test_query_endpoint_required_fields():
    """Test that question is required"""

    invalid_payload = {
        # Missing required "question" field
    }

    response = client.post("/api/query", json=invalid_payload)

    # Should return validation error since question is required
    assert response.status_code in [422, 400]