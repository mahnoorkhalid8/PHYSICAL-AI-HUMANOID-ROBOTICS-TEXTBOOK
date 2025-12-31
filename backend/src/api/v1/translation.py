from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from typing import Dict, Any
from ...models.translation import TranslationRequest, TranslationResponse
from ...auth.jwt_validator import get_jwt_validator, JWTValidator
from ...services.translation_service import TranslationService

router = APIRouter()
security = HTTPBearer()

# Initialize JWT validator and translation service
jwt_validator = get_jwt_validator()
translation_service = TranslationService()


async def auth_middleware(request: Request, call_next):
    """
    Authentication middleware for the translation endpoint
    """
    # Extract the authorization header
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid format"
        )

    token = auth_header[7:]  # Remove "Bearer " prefix

    try:
        # Validate the JWT token using the existing validator
        decoded_token = await jwt_validator.validate_token(token)

        # Add decoded token to request state for use in endpoints
        request.state.user = decoded_token

        response = await call_next(request)
        return response
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception:
        # For other exceptions, raise unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


@router.get("/translate/health")
async def translate_health():
    """
    Health check for the translation endpoint
    """
    return {"status": "translate endpoint is healthy"}


@router.post("/translate", response_model=TranslationResponse)
async def translate_content(
    request: TranslationRequest,
    token: HTTPAuthorizationCredentials = Depends(security)
) -> TranslationResponse:
    """
    Translate content from English to Urdu using AI
    """
    try:
        print(f"Received translation request with content length: {len(request.text) if request.text else 0}")

        # Validate the JWT token using the existing validator
        decoded_token = await jwt_validator.validate_token(token.credentials)
        print(f"Token validated successfully for user: {decoded_token.get('sub')}")

        # Extract user information from token
        token_user_id = decoded_token.get("sub")  # Subject is typically the user ID

        # Validate request text
        if not request.text or len(request.text.strip()) < 5:
            print(f"Text too short: {len(request.text) if request.text else 0} chars")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text must be at least 5 characters"
            )

        if len(request.text) > 50000:  # 50KB limit
            print(f"Text too long: {len(request.text)} chars")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text exceeds maximum length of 50KB"
            )

        print(f"Text validation passed, proceeding with translation")

        # Record start time for processing time calculation
        start_time = time.time()

        # Prepare the translation request
        translation_request_data = {
            "text": request.text,
            "target_language": request.target_language,
            "source_language": request.source_language,
            "context": request.context
        }

        # Perform the translation using the request object directly
        translation_result = await translation_service.translate_content(request)

        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)

        # Update processing time in the response metadata
        translation_result.translation_metadata.processing_time = processing_time

        print(f"Translation completed successfully in {processing_time}ms")
        return translation_result

    except HTTPException as he:
        # Re-raise HTTP exceptions as they are
        print(f"HTTP Exception in translate_content: {he.detail}")
        raise
    except Exception as e:
        # Log the error in a real application
        print(f"Error in translate_content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during translation"
        )