from datetime import datetime, timezone
from typing import Dict, Any, Optional
import httpx
from fastapi import HTTPException, status
from jose import jwt, jwk
from jose.constants import ALGORITHMS
from jose.exceptions import JWTError, ExpiredSignatureError
import json
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Configuration for JWT validation
JWT_ALGORITHM = "RS256"

# Import cryptography library to extract public key from private key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import base64

# Private key that matches the one used for signing tokens
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

def extract_public_key():
    """Extract public key from private key"""
    private_key = load_pem_private_key(PRIVATE_KEY_PEM.encode(), password=None)
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem.decode('utf-8')

# Local public key for validation (extracted from the private key used for signing)
LOCAL_PUBLIC_KEY_PEM = extract_public_key()

class JWTValidator:
    def __init__(self, jwks_url: str = None):
        """
        Initialize JWT validator with local public key
        :param jwks_url: Not used anymore, kept for compatibility
        """
        # Use local public key for validation
        self.local_public_key = jwk.construct(LOCAL_PUBLIC_KEY_PEM.encode(), ALGORITHMS.RS256)

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate the JWT token using the local public key
        :param token: JWT token to validate
        :return: Decoded token payload
        """
        try:
            # Decode and verify the token using local public key
            decoded_token = jwt.decode(
                token,
                self.local_public_key,
                algorithms=[JWT_ALGORITHM],
                options={"verify_aud": False, "verify_exp": True, "verify_nbf": True}  # Verify expiration and not-before
            )

            return decoded_token

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error during token validation: {str(e)}"
            )

    def get_user_background_from_token(self, decoded_token: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract user background information from the decoded token
        :param decoded_token: Decoded JWT token
        :return: Dictionary with user background information
        """
        user_metadata = decoded_token.get("user_metadata", {})

        # Handle different possible structures for user metadata
        software_background = user_metadata.get("software_background", "")
        hardware_background = user_metadata.get("hardware_background", "")

        # Fallback: check directly in the token if not in user_metadata
        if not software_background:
            software_background = decoded_token.get("software_background", "")
        if not hardware_background:
            hardware_background = decoded_token.get("hardware_background", "")

        return {
            "software": software_background,
            "hardware": hardware_background
        }

# Initialize JWT validator with local validation
def get_jwt_validator() -> JWTValidator:
    # Use local validation with embedded public key, no external JWKS needed
    return JWTValidator()