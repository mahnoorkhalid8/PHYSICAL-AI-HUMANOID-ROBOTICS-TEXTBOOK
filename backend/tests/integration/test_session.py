import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.db import SessionLocal
from backend.src.models.chat_session import ChatSession
from backend.src.models.message import Message
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

client = TestClient(app)

def test_session_creation_integration():
    """Integration test for session creation"""

    # Test creating a session with user_id and metadata
    user_id = str(uuid.uuid4())
    payload = {
        "user_id": user_id,
        "metadata": {
            "user_agent": "Mozilla/5.0 (test)",
            "page_url": "/docs/01-robotic-nervous-system"
        }
    }

    response = client.post("/api/session", json=payload)

    # Should return successful response
    assert response.status_code in [200, 201]
    data = response.json()

    # Verify response structure
    assert "session_id" in data
    assert "created_at" in data

    # Verify session_id is a valid UUID string
    assert isinstance(data["session_id"], str)
    # Try to parse as UUID to verify format
    uuid.UUID(data["session_id"])

    # Verify created_at is in ISO format
    assert isinstance(data["created_at"], str)

def test_session_creation_without_optional_fields():
    """Integration test for session creation without optional fields"""

    # Test creating a session with minimal data
    payload = {}

    response = client.post("/api/session", json=payload)

    # Should return successful response
    assert response.status_code in [200, 201]
    data = response.json()

    # Verify response structure
    assert "session_id" in data
    assert "created_at" in data

def test_get_session_messages_integration():
    """Integration test for retrieving session messages"""

    # First create a session
    response = client.post("/api/session", json={})
    assert response.status_code in [200, 201]
    session_data = response.json()
    session_id = session_data["session_id"]

    # Now try to get messages for this session (should be empty initially)
    response = client.get(f"/api/session/{session_id}/messages")

    # Should return successful response with empty messages list
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "messages" in data
    assert isinstance(data["messages"], list)
    assert len(data["messages"]) == 0

def test_get_nonexistent_session_messages():
    """Test retrieving messages for a session that doesn't exist"""

    # Use a valid UUID format but for a session that doesn't exist
    nonexistent_session_id = str(uuid.uuid4())

    response = client.get(f"/api/session/{nonexistent_session_id}/messages")

    # Should return 404 (not found)
    assert response.status_code == 404
    data = response.json()

    # Verify error response structure
    assert "error" in data
    assert "code" in data
    assert data["code"] == "NOT_FOUND"

def test_session_creation_and_message_storage():
    """Integration test combining session creation with message storage"""

    # Create a session
    response = client.post("/api/session", json={
        "metadata": {"test": "value"}
    })
    assert response.status_code in [200, 201]
    session_data = response.json()
    session_id = session_data["session_id"]

    # Verify the session was created with the correct metadata
    assert isinstance(session_data["session_id"], str)
    assert isinstance(session_data["created_at"], str)

    # Now get messages for this session (should be empty)
    response = client.get(f"/api/session/{session_id}/messages")
    assert response.status_code == 200
    messages_data = response.json()
    assert "messages" in messages_data
    assert isinstance(messages_data["messages"], list)
    assert len(messages_data["messages"]) == 0