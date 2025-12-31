#!/usr/bin/env python3
"""
Simple mock JWKS server for testing the personalization API
"""
from flask import Flask, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import json
import base64

app = Flask(__name__)

# Generate a test RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Convert the public key to JWK format manually
public_numbers = public_key.public_numbers()

# Convert to base64url encoding (no padding)
def int_to_base64url(n):
    """Convert integer to base64url format"""
    # Convert to bytes
    byte_length = (n.bit_length() + 7) // 8
    b = n.to_bytes(byte_length, 'big')
    # Encode to base64 and remove padding
    b64 = base64.b64encode(b).decode('utf-8')
    # Convert to base64url (replace + with -, / with _)
    b64url = b64.replace('+', '-').replace('/', '_')
    # Remove padding
    b64url = b64url.rstrip('=')
    return b64url

# Create JWK manually
jwk_dict = {
    "kty": "RSA",
    "use": "sig",
    "kid": "test-key-id",
    "alg": "RS256",
    "n": int_to_base64url(public_numbers.n),
    "e": int_to_base64url(public_numbers.e)
}

# Save private key for token generation
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

@app.route('/auth/jwks', methods=['GET'])
def get_jwks():
    """Return the JWKS with the test key"""
    jwks = {
        "keys": [jwk_dict]
    }
    return jsonify(jwks)

@app.route('/auth/private-key', methods=['GET'])
def get_private_key():
    """Return the private key (for testing only - never do this in production)"""
    return jsonify({
        "private_key": private_pem.decode('utf-8'),
        "kid": "test-key-id"
    })

if __name__ == '__main__':
    print("Starting mock JWKS server on http://localhost:4000")
    print("JWKS endpoint: http://localhost:4000/auth/jwks")
    print("Test key ID: test-key-id")
    print("\nJWK:")
    print(json.dumps(jwk_dict, indent=2))
    app.run(host='localhost', port=4000, debug=False)