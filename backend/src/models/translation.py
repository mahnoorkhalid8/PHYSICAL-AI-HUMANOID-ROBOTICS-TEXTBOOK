from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TranslationRequest(BaseModel):
    """Represents a user's request to translate content"""
    text: str = Field(..., description="The original English content to be translated", max_length=50000)  # ~50KB limit
    source_language: str = Field("en", description="Source language (default: 'en')")
    target_language: str = Field("ur", description="Target language (default: 'ur')")
    context: Optional[str] = Field(None, description="Additional context for translation")
    preserve_technical_terms: bool = Field(True, description="Whether to preserve technical terms in English")
    language_from: str = Field("en", description="Source language (default: 'en')")
    language_to: str = Field("ur", description="Target language (default: 'ur')")


class TranslationMetadata(BaseModel):
    """Metadata about the translation process"""
    processing_time: int = Field(..., description="Time taken for translation in milliseconds", ge=0)
    token_count: int = Field(..., description="Number of tokens in the content", ge=0)
    confidence_score: float = Field(..., description="Confidence level of the translation", ge=0.0, le=1.0)


class TranslationResponse(BaseModel):
    """Represents the translated content response"""
    original_content: str = Field(..., description="The original English content")
    translated_content: str = Field(..., description="The translated Urdu content")
    language_from: str = Field("en", description="Source language (default: 'en')")
    language_to: str = Field("ur", description="Target language (default: 'ur')")
    translation_metadata: TranslationMetadata = Field(..., description="Additional information about the translation")


class TranslationSessionState(str, Enum):
    """Possible states for a translation session"""
    INITIAL = "initial"
    CONTENT_EXTRACTED = "content_extracted"
    TRANSLATION_REQUESTED = "translation_requested"
    TRANSLATING = "translating"
    TRANSLATION_SUCCESS = "translation_success"
    TRANSLATION_ERROR = "translation_error"


class TranslationSession(BaseModel):
    """Represents the state of a translation session in the UI"""
    session_id: str = Field(..., description="Unique identifier for the session")
    original_content: str = Field(..., description="The original content being translated")
    translated_content: Optional[str] = Field(None, description="Cached translated content (if available)")
    is_translating: bool = Field(False, description="Whether translation is in progress")
    translation_error: Optional[str] = Field(None, description="Error message if translation failed")
    view_mode: str = Field("original", description="Current view mode (original, translated, side-by-side)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the session was created")