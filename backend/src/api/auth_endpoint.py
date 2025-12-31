from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from typing import Dict, Any
from datetime import datetime, timedelta
from jose import jwt as jose_jwt, jwk
from jose.constants import ALGORITHMS
from jose.exceptions import JWTError, ExpiredSignatureError
import json
import base64

# Private key for signing tokens (in production, this should be securely stored)
PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDG+MWXMRq3uxGh
pH5xQtSPvUwVcCC45xKqs8DIMsPEb6euRo+JdomnvNC3IuZPH7MBTFm7KPXjpgd+
IYOvBu57Kyh+0XLwZet8wLgoiNnxh5x0z60qm+eCt0HL4JzQGXduSo90ngCY06FP
X5vBXB+MQUTpRt1v8uyafrbK4WmCVp7a7IaFcKGM471Ue89lOBpkP1eph3KlAmGV
WA10cPV7om0h5ZT8sGCSh2pnTXiOarEuQN9ugH1Xd1fCfTOXwPh3S3KCGSH35dWd
rfyQ+GGkqPHojoG16CePBuUAAGQluGjdW+F3v7V1myyzybynLKmVibiJn6dwfmHC
jodEJZkFAgMBAAECggEAQkAkHocBo+qcYMuSNGkxuJippDu9EYQTMZZ/mslYaOha
l0s0UOuQwzK59jifIfpmkoiXGhv137JxLTzAiX9P2eARcESSNlxhUB0lVI3Yr7Td
UgGyYY0exWX6eQWVgS7xlt4prQVNIpXY0MJ/bJ8dfAhhhyEK61MiGAEYIS50AKr7
Qhy04xLpSFi+OQlcZmX7dtOck5uSrVmUBPLtXMkl6PuIwLSoYK6J0oSlOTgFlvjB
7Pr6k5LNB+J+dEp4zAQ3MExq7Vvs5YA7KDHlXqRJNTbNP8CSNkBx4Jnj/5FfzwTN
k9pup7ertKAE2LC8QU/jX56rL3vKnFO1SsQPhCAGkwKBgQDxLJYx4eCLhaajzurR
f0FJAMpWK0uFnXkJ/IUeTFVlq0neyTlt4XlNBb+zaC/fjz1bM3nTQEtZNsowRypM
jtZH3Uvi8NHb8AayPsebh52V4yFkzMgyTPhOp+xg3zkB1DxBk4IWZdZIWD22O7Zv
1eUJgtKBUVTLv91SUaLqwkMStwKBgQDTNAlHHvIm2SmnYdlDxjPM1UIQDiSrrgQS
xITMZkLjteLVQsJNCsq9x6fBWGnNWtHjvyiux3bQKCqsBXy2cuG/fR0sqVLuhSa+
5Y9Uh7+hXrDqxcXUYht4MvTl0rB0yPawOSCX0aYAA4GRI2VnaZC6bw3hAkHV4yc3
DY/NhQRGIwKBgFksSzyWcBgmir72uwxLKTB9AlNqHrqAx0hR/kZ9ovW8p8ugS4O9
YsR/46nKVCktJVqbZegeVb3e7FN9fL5h8gkQYga/VFkmHtO5MsTnF/VbzfUfYsZ2
fzlWDaij4Mg0WTNF/0uYy+pj9i1zVrlzNQSXQo5eLCRKBONzG/IBchtxAoGAYFaO
HNjqz/mi3Gzvs9CG9FoahkRNSdpYlU763FmRDVl8HJcVFhtkG2klBjaUHE3fC6m4
nvDxK0YHIOxn1LlWbAhf9G1QHOizocQIuyAosy0EOjL4aEZQDWYA+4w9XSgGDqAg
U+AXfk4bHd8tdBxdHg1mIUrsSOoSizQucirIpk0CgYBl1Blg8Y+XbVOuauvOrZ5v
dLgN+MyQdig6vBkkPFa19rYMz/3K8+XpXTjHuQuzpMCVXw/WnIrWHL4o9PvVXdNr
r0NPa2TW7Ex322Fx+sF6fPrJhTMCk2CG/KgkgVaSmcO52nVFkH+btTf1XQJQ6QLF
PiZ+zJQwumL2uxUwV6d2Zg==
-----END PRIVATE KEY-----"""

# Extract public key from private key for JWKS
def extract_public_key():
    """Extract the public key from the private key to create JWKS"""
    try:
        # Create a key from the private key PEM
        signing_key = jwk.construct(PRIVATE_KEY_PEM, ALGORITHMS.RS256)
        # Get the public key representation
        public_key = signing_key.public_key()
        # Get the public key in JWK format
        jwk_dict = public_key.to_dict()
        # Add the key ID and use
        jwk_dict["kid"] = "test-key-id"
        jwk_dict["use"] = "sig"
        jwk_dict["alg"] = "RS256"
        return jwk_dict
    except Exception as e:
        print(f"Error extracting public key: {e}")
        return None

# Create the JWKS
PUBLIC_JWK = extract_public_key()
JWKS = {
    "keys": [PUBLIC_JWK] if PUBLIC_JWK else []
}

router = APIRouter()
security = HTTPBearer()

# In a real application, you would store refresh tokens securely
# This is a simplified implementation for demonstration purposes
active_tokens = set()  # This would be a database in production

@router.post("/auth/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Refresh an expired JWT token
    """
    try:
        token = credentials.credentials

        # Decode the token without verification to extract user data
        # In a real app, you'd have a separate refresh token system
        # This is a simplified approach for the demo
        try:
            # Get the header without verification
            header = jose_jwt.get_unverified_header(token)
            payload = jose_jwt.decode(
                token,
                PRIVATE_KEY_PEM,
                algorithms=[ALGORITHMS.RS256],
                options={"verify_exp": False}  # Don't verify expiration for refresh
            )

            # Create a new token with updated expiration (30 minutes from now)
            new_payload = {
                "sub": payload.get("sub", "unknown"),
                "email": payload.get("email", ""),
                "name": payload.get("name", ""),
                "user_metadata": payload.get("user_metadata", {}),
                "iat": int(datetime.utcnow().timestamp()),
                "exp": int((datetime.utcnow() + timedelta(minutes=30)).timestamp()),
                "nbf": int(datetime.utcnow().timestamp()),
                "iss": payload.get("iss", "test-auth-server"),
                "aud": payload.get("aud", "test-app"),
                "kid": "test-key-id"
            }

            # Generate new token using jose library
            new_token = jose_jwt.encode(
                new_payload,
                PRIVATE_KEY_PEM,
                ALGORITHMS.RS256,
                headers={"kid": "test-key-id"}
            )

            # Add new token to active tokens set
            active_tokens.add(new_token)

            return {
                "token": new_token,
                "expires_in": 1800,  # 30 minutes in seconds
                "token_type": "Bearer"
            }

        except jose_jwt.JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.get("/auth/jwks")
async def get_jwks():
    """
    JWKS endpoint that returns the public key for token validation
    """
    return JWKS

@router.post("/auth/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify if a token is valid
    """
    try:
        token = credentials.credentials

        # Use the jose library for decoding - verify with the same key that was used for signing
        # In RS256, the public key is derived from the private key for verification
        decoded_token = jose_jwt.decode(
            token,
            PRIVATE_KEY_PEM,
            algorithms=[ALGORITHMS.RS256],
            options={"verify_aud": False, "verify_exp": True, "verify_nbf": True}
        )

        return {
            "valid": True,
            "user_id": decoded_token.get("sub"),
            "expires_at": decoded_token.get("exp")
        }

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jose_jwt.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token verification failed: {str(e)}"
        )