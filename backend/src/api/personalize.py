from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from typing import Dict, Any
from ..models.personalization import PersonalizeRequest, PersonalizeResponse
from ..auth.jwt_validator import get_jwt_validator, JWTValidator
from ..services.personalization_service import PersonalizationService

router = APIRouter()
security = HTTPBearer()

# Initialize JWT validator
jwt_validator = get_jwt_validator()
personalization_service = PersonalizationService()

async def auth_middleware(request: Request, call_next):
    """
    Authentication middleware for the personalization endpoint
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
        # Validate the JWT token
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

@router.post("/personalize", response_model=PersonalizeResponse)
async def personalize_content(
    request: PersonalizeRequest,
    token: HTTPAuthorizationCredentials = Depends(security)
) -> PersonalizeResponse:
    """
    Generate personalized content based on user background and chapter content
    """
    try:
        # Validate the JWT token
        decoded_token = await jwt_validator.validate_token(token.credentials)

        # Extract user background from token
        user_background = jwt_validator.get_user_background_from_token(decoded_token)

        # Verify that the user_id in the request matches the token's user
        token_user_id = decoded_token.get("sub")  # Subject is typically the user ID
        if request.user_id != token_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID in request does not match authenticated user"
            )

        # Validate request content
        if not request.chapter_content or len(request.chapter_content.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chapter content must be at least 10 characters"
            )

        if not user_background.get("software") or not user_background.get("hardware"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User background information is required"
            )

        # Record start time for processing time calculation
        start_time = time.time()

        # Generate personalized content
        personalized_result = await personalization_service.generate_personalized_content(
            chapter_content=request.chapter_content,
            chapter_title=request.chapter_title,
            user_background=user_background
        )

        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)

        # Create and return response
        response = PersonalizeResponse(
            id=f"personalize-{int(time.time())}",
            personalized_content=personalized_result["content"],
            personalization_reasoning=personalized_result["reasoning"],
            generated_at=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            processing_time_ms=processing_time
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Log the error in a real application
        print(f"Error in personalize_content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during personalization"
        )

# Add rate limiting middleware
