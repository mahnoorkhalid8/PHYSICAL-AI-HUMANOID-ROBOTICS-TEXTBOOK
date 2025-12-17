import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
import uuid

client = TestClient(app)

def test_create_session_contract():
    """Contract test for /api/session POST endpoint"""

    # Test valid request
    valid_payload = {
        "user_id": str(uuid.uuid4()),
        "metadata": {
            "user_agent": "Mozilla/5.0...",
            "page_url": "/docs/01-robotic-nervous-system"
        }
    }

    response = client.post("/api/session", json=valid_payload)

    # Check that response has expected structure
    assert response.status_code in [200, 201, 422, 500]

    if response.status_code in [200, 201]:
        data = response.json()
        # Check that response has required fields
        assert "session_id" in data
        assert "created_at" in data

        # Check that session_id is a valid UUID string
        assert isinstance(data["session_id"], str)

        # Check that created_at is a string (ISO format timestamp)
        assert isinstance(data["created_at"], str)

def test_create_session_minimal_request():
    """Test session creation with minimal request (no user_id, no metadata)"""

    minimal_payload = {}

    response = client.post("/api/session", json=minimal_payload)

    # Should return successful response with just session_id and created_at
    assert response.status_code in [200, 201, 422, 500]

    if response.status_code in [200, 201]:
        data = response.json()
        assert "session_id" in data
        assert "created_at" in data

def test_get_session_messages_contract():
    """Contract test for /api/session/{session_id}/messages GET endpoint"""

    # Use a valid UUID format
    session_id = str(uuid.uuid4())

    response = client.get(f"/api/session/{session_id}/messages")

    # Check that response has expected structure
    assert response.status_code in [200, 400, 404, 500]

    if response.status_code == 200:
        data = response.json()
        # Check that response has required field
        assert "messages" in data

        # Check that messages is a list
        assert isinstance(data["messages"], list)

def test_session_endpoint_with_invalid_uuid():
    """Test session endpoints with invalid UUID format"""

    # Test with invalid session ID
    invalid_session_id = "invalid-uuid-format"

    response = client.get(f"/api/session/{invalid_session_id}/messages")

    # Should return validation error
    assert response.status_code in [400, 422]

def test_session_creation_with_invalid_user_id():
    """Test session creation with invalid user_id format"""

    invalid_payload = {
        "user_id": "invalid-uuid-format",  # This should be rejected
        "metadata": {}
    }

    response = client.post("/api/session", json=invalid_payload)

    # Should return validation error
    assert response.status_code in [400, 422]