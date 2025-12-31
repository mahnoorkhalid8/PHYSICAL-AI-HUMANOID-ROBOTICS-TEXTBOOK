#!/usr/bin/env python3
"""
Generate a proper JWT token that matches the JWKS server key
"""
import jwt
import json
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64

# Generate the same RSA key pair as the JWKS server
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

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
    "kid": "test-key-id"  # Key ID (must match JWKS)
}

# Generate the RS256 token
token = jwt.encode(payload, private_pem, algorithm="RS256", headers={"kid": "test-key-id"})

print("Generated JWT Token (RS256):")
print(token)
print("\nPayload:")
print(json.dumps(payload, indent=2))

# Also print the public key for verification
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("\nPublic Key (PEM format):")
print(public_pem.decode())

# Convert to JWK format for verification
def int_to_base64url(n):
    """Convert integer to base64url format"""
    byte_length = (n.bit_length() + 7) // 8
    b = n.to_bytes(byte_length, 'big')
    b64 = base64.b64encode(b).decode('utf-8')
    b64url = b64.replace('+', '-').replace('/', '_')
    b64url = b64url.rstrip('=')
    return b64url

public_numbers = public_key.public_numbers()
jwk_dict = {
    "kty": "RSA",
    "use": "sig",
    "kid": "test-key-id",
    "alg": "RS256",
    "n": int_to_base64url(public_numbers.n),
    "e": int_to_base64url(public_numbers.e)
}

print("\nPublic JWK (should match JWKS):")
print(json.dumps(jwk_dict, indent=2))