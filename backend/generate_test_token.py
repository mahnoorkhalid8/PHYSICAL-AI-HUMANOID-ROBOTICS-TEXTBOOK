#!/usr/bin/env python3
"""
Script to generate a test JWT token for the personalization API
"""
import jwt
import json
from datetime import datetime, timedelta
from jose import jwk
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def generate_test_token():
    """
    Generate a test JWT token that matches the expected structure for the personalization API
    """
    # Define the payload structure expected by the system
    payload = {
        "sub": "test-user-123",  # User ID
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
        "aud": "test-app"  # Audience
    }

    # Note: Since the system expects RS256 with JWKS, we need to use a proper RSA key
    # For testing purposes, we'll create a simple token with HS256 since we have a secret
    # But we'll structure it to match the expected format

    # Using HS256 with the secret from the environment
    secret = os.getenv("JWT_SECRET", "default-secret-for-testing")

    # Generate the token
    token = jwt.encode(payload, secret, algorithm="HS256")

    print("Generated Test JWT Token:")
    print(token)
    print("\nPayload:")
    print(json.dumps(payload, indent=2))

    return token

def generate_rs256_token():
    """
    Generate an RS256 token with a test key (for proper testing)
    """
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    # Generate a test RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Get the private key in PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Define the payload
    payload = {
        "sub": "test-user-123",  # User ID
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
        "kid": "test-key-id"  # Key ID
    }

    # Generate the RS256 token
    token = jwt.encode(payload, private_pem, algorithm="RS256", headers={"kid": "test-key-id"})

    print("\nGenerated Test JWT Token (RS256):")
    print(token)
    print("\nPayload:")
    print(json.dumps(payload, indent=2))

    # Also print the public key in JWK format for reference
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Convert to JWK format
    jwk_obj = jwk.construct(public_pem)
    jwk_dict = jwk_obj.to_dict()
    jwk_dict['kid'] = 'test-key-id'

    print("\nPublic JWK (for JWKS):")
    print(json.dumps(jwk_dict, indent=2))

    return token

if __name__ == "__main__":
    print("Generating test tokens for the personalization API...")

    # First, try with HS256 (using the secret from .env)
    hs256_token = generate_test_token()

    # Then, generate RS256 for proper testing
    try:
        rs256_token = generate_rs256_token()
    except ImportError:
        print("\nCryptography library not available, skipping RS256 token generation")
        print("Install with: pip install cryptography")
        rs256_token = None

    print("\nUse one of these tokens for testing the personalization API:")
    print(f"HS256 Token: {hs256_token}")
    if rs256_token:
        print(f"RS256 Token: {rs256_token}")