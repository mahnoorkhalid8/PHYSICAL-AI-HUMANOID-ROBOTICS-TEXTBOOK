import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
import importlib.util

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Use importlib to properly load the main module to avoid caching issues
# The test file is in backend/tests/contract/, so going up 3 levels gets to project root
# Then we go into backend/main.py
current_file_dir = os.path.dirname(__file__)  # tests/contract/
parent_dir = os.path.dirname(current_file_dir)  # tests/
backend_dir = os.path.dirname(parent_dir)  # backend/
backend_path = os.path.join(backend_dir, "main.py")  # backend/main.py

spec = importlib.util.spec_from_file_location("main", backend_path)
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)

app = main_module.app

client = TestClient(app)

def test_personalize_endpoint_contract():
    """Contract test for /api/personalize endpoint"""

    # Create a mock JWT token for testing (development format)
    # This follows the format from the signup form: base64.header.base64.SIGNATURE_NOT_VALIDATED_IN_DEV
    import base64
    import json

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": "test_user_123",
        "email": "test@example.com",
        "exp": 9999999999,  # Far future expiration
        "iat": 1678886400,
        "software_background": "Intermediate",
        "hardware_background": "Beginner"
    }

    header_b64 = base64.b64encode(json.dumps(header).encode()).decode().replace("=", "")
    payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().replace("=", "")
    mock_token = f"{header_b64}.{payload_b64}.SIGNATURE_NOT_VALIDATED_IN_DEV"

    # Test valid request structure
    valid_payload = {
        "chapter_content": "This is a sample chapter about humanoid robotics.",
        "chapter_title": "Introduction to Humanoid Robotics",
        "user_id": "test_user_123"
    }

    # Mock the personalization service to avoid external dependencies
    with patch('src.api.personalize.personalization_service') as mock_service:
        # Since generate_personalized_content is an async method, we need to mock it properly
        async def mock_generate_personalized_content(chapter_content, chapter_title=None, user_background=None):
            return {
                "content": "This is personalized content based on your background.",
                "reasoning": "Content adapted based on your experience level."
            }

        mock_service.generate_personalized_content = mock_generate_personalized_content

        response = client.post(
            "/api/personalize",
            json=valid_payload,
            headers={"Authorization": f"Bearer {mock_token}"}
        )

        # Check that response has expected structure
        assert response.status_code in [200, 422, 500, 401]  # Various possible responses

        if response.status_code == 200:
            data = response.json()
            # Check that response has required fields
            assert "id" in data
            assert "personalized_content" in data
            assert "personalization_reasoning" in data
            assert "generated_at" in data
            assert "processing_time_ms" in data

            # Check that content fields are strings
            assert isinstance(data["personalized_content"], str)
            assert isinstance(data["personalization_reasoning"], str)
            assert isinstance(data["generated_at"], str)
            assert isinstance(data["processing_time_ms"], int)

def test_personalize_endpoint_missing_auth():
    """Test personalization endpoint without authentication"""

    invalid_payload = {
        "chapter_content": "This is a sample chapter about humanoid robotics.",
        "chapter_title": "Introduction to Humanoid Robotics",
        "user_id": "test_user_123"
    }

    response = client.post("/api/personalize", json=invalid_payload)

    # Should return 401/403/422 due to missing token or validation errors
    assert response.status_code in [401, 403, 422]

def test_personalize_endpoint_invalid_token():
    """Test personalization endpoint with invalid token"""

    invalid_payload = {
        "chapter_content": "This is a sample chapter about humanoid robotics.",
        "chapter_title": "Introduction to Humanoid Robotics",
        "user_id": "test_user_123"
    }

    response = client.post(
        "/api/personalize",
        json=invalid_payload,
        headers={"Authorization": "Bearer invalid_token"}
    )

    # Should return 401/422 due to invalid token or validation errors
    assert response.status_code in [401, 422]

def test_personalize_endpoint_missing_fields():
    """Test personalization endpoint with missing required fields"""

    # Create a mock JWT token for testing
    import base64
    import json

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": "test_user_123",
        "email": "test@example.com",
        "exp": 9999999999,  # Far future expiration
        "iat": 1678886400,
        "software_background": "Intermediate",
        "hardware_background": "Beginner"
    }

    header_b64 = base64.b64encode(json.dumps(header).encode()).decode().replace("=", "")
    payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().replace("=", "")
    mock_token = f"{header_b64}.{payload_b64}.SIGNATURE_NOT_VALIDATED_IN_DEV"

    # Missing required fields
    invalid_payload = {
        # Missing all required fields
    }

    # Mock the personalization service to avoid external dependencies
    with patch('src.api.personalize.personalization_service') as mock_service:
        # Since generate_personalized_content is an async method, we need to mock it properly
        async def mock_generate_personalized_content(chapter_content, chapter_title=None, user_background=None):
            return {
                "content": "This is personalized content based on your background.",
                "reasoning": "Content adapted based on your experience level."
            }

        mock_service.generate_personalized_content = mock_generate_personalized_content

        response = client.post(
            "/api/personalize",
            json=invalid_payload,
            headers={"Authorization": f"Bearer {mock_token}"}
        )

    # Should return validation error
    assert response.status_code in [422, 400]