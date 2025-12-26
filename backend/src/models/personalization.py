from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class PersonalizeRequest(BaseModel):
    """
    Request model for personalization API
    """
    chapter_content: str = Field(
        ...,
        description="The full content of the chapter to personalize",
        min_length=10
    )
    chapter_title: Optional[str] = Field(
        None,
        description="The title of the chapter (optional)"
    )
    user_id: str = Field(
        ...,
        description="The authenticated user's ID"
    )
    user_background: Dict[str, str] = Field(
        ...,
        description="User's background information",
        example={"software": "Intermediate Python developer", "hardware": "Basic electronics knowledge"}
    )

    class Config:
        schema_extra = {
            "example": {
                "chapter_content": "This chapter covers the fundamentals of humanoid robotics...",
                "chapter_title": "Introduction to Humanoid Robotics",
                "user_id": "user-12345",
                "user_background": {
                    "software": "Intermediate Python developer with robotics experience",
                    "hardware": "Basic understanding of electronic circuits"
                }
            }
        }

class PersonalizeResponse(BaseModel):
    """
    Response model for personalization API
    """
    id: str = Field(
        ...,
        description="Unique identifier for this personalization response"
    )
    personalized_content: str = Field(
        ...,
        description="The AI-generated personalized content"
    )
    personalization_reasoning: str = Field(
        ...,
        description="Brief explanation of personalization approach"
    )
    generated_at: str = Field(
        ...,
        description="ISO 8601 timestamp of generation"
    )
    processing_time_ms: int = Field(
        ...,
        description="Time taken to process the request in milliseconds"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "personalize-67890",
                "personalized_content": "Since you have intermediate Python experience with robotics...",
                "personalization_reasoning": "Content adapted based on user's Python skills and robotics experience",
                "generated_at": "2025-12-25T10:30:00Z",
                "processing_time_ms": 1250
            }
        }

class UserBackground(BaseModel):
    """
    Model for user background information
    """
    software: str = Field(
        ...,
        description="User's software background",
        min_length=2,
        max_length=200
    )
    hardware: str = Field(
        ...,
        description="User's hardware background",
        min_length=2,
        max_length=200
    )