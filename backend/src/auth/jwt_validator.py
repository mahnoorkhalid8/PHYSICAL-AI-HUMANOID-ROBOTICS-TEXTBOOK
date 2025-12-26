from datetime import datetime, timezone
from typing import Dict, Any, Optional
import httpx
from fastapi import HTTPException, status
from jose import jwt, jwk
from jose.constants import ALGORITHMS
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

class JWTValidator:
    def __init__(self, jwks_url: str):
        """
        Initialize JWT validator with JWKS URL
        :param jwks_url: URL to the JWKS endpoint
        """
        self.jwks_url = jwks_url
        self.jwks_client = httpx.Client()

    async def get_jwks(self) -> Dict[str, Any]:
        """
        Fetch JWKS from the provided URL
        :return: JSON Web Key Set
        """
        try:
            response = self.jwks_client.get(self.jwks_url)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to fetch JWKS: {str(e)}"
            )

    async def get_signing_key(self, token_kid: str) -> jwk.RSAKey:
        """
        Get the signing key for the given key ID from the JWKS
        :param token_kid: Key ID from the token header
        :return: RSA signing key
        """
        jwks = await self.get_jwks()

        # Find the key with the matching kid
        keys = jwks.get("keys", [])
        for key in keys:
            if key.get("kid") == token_kid:
                # Create and return the RSA key
                return jwk.construct(key, ALGORITHMS.RS256)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unable to find signing key for kid: {token_kid}"
        )

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate the JWT token using RS256 algorithm and JWKS
        :param token: JWT token to validate
        :return: Decoded token payload
        """
        try:
            # Decode the token header to get the kid
            header = jwt.get_unverified_header(token)
            token_kid = header.get("kid")

            if not token_kid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token header missing kid"
                )

            # Get the JWKS to verify the token
            jwks = await self.get_jwks()

            # Find the matching key in JWKS
            key_to_verify = None
            for key in jwks.get("keys", []):
                if key.get("kid") == token_kid:
                    key_to_verify = key
                    break

            if not key_to_verify:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Signing key not found in JWKS"
                )

            # Decode and verify the token using RS256
            decoded_token = jwt.decode(
                token,
                key_to_verify,
                algorithms=[JWT_ALGORITHM],
                options={"verify_aud": False, "verify_exp": True, "verify_nbf": True}  # Verify expiration and not-before
            )

            return decoded_token

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError as e:
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

# Initialize JWT validator with the JWKS URL from environment
def get_jwt_validator() -> JWTValidator:
    jwks_url = os.getenv("BETTER_AUTH_JWKS_URL", "")
    if not jwks_url:
        raise ValueError("BETTER_AUTH_JWKS_URL environment variable is required")

    return JWTValidator(jwks_url)