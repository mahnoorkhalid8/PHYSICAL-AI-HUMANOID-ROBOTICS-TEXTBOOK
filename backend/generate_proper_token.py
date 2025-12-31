#!/usr/bin/env python3
"""
Generate a proper JWT token using the private key from the JWKS server
"""
import jwt
import json
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
import requests

# Get the private key from the JWKS server
response = requests.get('http://localhost:4000/auth/private-key')
private_key_data = response.json()
private_key_pem = private_key_data['private_key']
kid = private_key_data['kid']

# Define the payload that matches what the system expects
payload = {
    "sub": "test-user-123",  # User ID (matches the user_id in the request)
    "email": "test@example.com",
    "name": "Test User",
    "user_metadata": {
        "software_background": "Intermediate Python developer with robotics experience",
        "hardware_background": "Basic understanding of electronic circuits"
    },
    "iat": int(datetime.utcnow().timestamp()),  # Issued at
    "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp()),  # Expires in 24 hours
    "nbf": int(datetime.utcnow().timestamp()),  # Not before
    "iss": "test-auth-server",  # Issuer
    "aud": "test-app",  # Audience
    "kid": kid  # Key ID (must match JWKS)
}

# Generate the RS256 token using the private key
token = jwt.encode(payload, private_key_pem, algorithm="RS256", headers={"kid": kid})

print("Generated Proper JWT Token (RS256):")
print(token)
print("\nPayload:")
print(json.dumps(payload, indent=2))

# Also create a sample request body for the API
request_body = {
    "chapter_content": "This chapter covers the fundamentals of humanoid robotics, including kinematics, dynamics, control systems, and gait planning. We'll explore how robots can mimic human movement patterns and maintain balance while walking. The chapter includes mathematical models for legged locomotion, sensor fusion techniques, and real-time control algorithms.",
    "chapter_title": "Introduction to Humanoid Robotics",
    "user_id": "test-user-123",
    "user_background": {
        "software": "Intermediate Python developer with robotics experience",
        "hardware": "Basic understanding of electronic circuits"
    }
}

print("\nSample request body for personalization API:")
print(json.dumps(request_body, indent=2))

print("\nComplete curl command:")
print(f'curl -X POST http://localhost:8000/api/personalize -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d \'{json.dumps(request_body)}\'')