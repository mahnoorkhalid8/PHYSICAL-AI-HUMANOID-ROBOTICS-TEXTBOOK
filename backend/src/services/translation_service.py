from typing import Dict, Any, Optional
import time
import os
from groq import AsyncGroq
from ..models.translation import TranslationRequest, TranslationResponse, TranslationMetadata


class TranslationService:
    def __init__(self):
        """
        Initialize the translation service with Groq API client
        """
        # Get the GROQ_API_KEY from environment variables
        groq_api_key = os.getenv("GROQ_API_KEY")

        # If no API key is set, use mock mode for testing
        if not groq_api_key:
            print("GROQ_API_KEY not found, using mock translation service for testing")
            self.use_mock = True
        else:
            self.use_mock = False
            # Get the model name from environment variables, default to llama3-70b-8192
            self.model_name = os.getenv("GROQ_MODEL_NAME", "llama3-70b-8192")
            self.client = AsyncGroq(api_key=groq_api_key)

    async def translate_content(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate content using the Groq API with proper prompt engineering
        """
        start_time = time.time()

        try:
            print(f"Starting translation for content of length: {len(request.text)}")
            print(f"Request parameters: {request.source_language} -> {request.target_language}, preserve_technical_terms: {request.preserve_technical_terms}")

            if self.use_mock:
                # Mock translation for testing purposes
                print("Using mock translation service")

                # Simple mock translation - just return the original text with a prefix
                mock_translation = f"[URDU MOCK] {request.text} [TRANSLATED]"

                # Calculate processing time
                processing_time = int((time.time() - start_time) * 1000)

                # Create translation metadata
                metadata = TranslationMetadata(
                    processing_time=processing_time,
                    token_count=len(request.text.split()),  # Simple token count estimation
                    confidence_score=0.95  # High confidence for mock response
                )

                # Create and return the response
                response = TranslationResponse(
                    original_content=request.text,
                    translated_content=mock_translation,
                    language_from=request.source_language,
                    language_to=request.target_language,
                    translation_metadata=metadata
                )

                print(f"Mock translation completed successfully in {processing_time}ms")
                return response
            else:
                # Create a system prompt for Urdu translation that preserves technical terms
                system_prompt = """You are an expert translator specializing in technical educational content. Translate the provided text from English to Urdu.
- Preserve all technical terms (especially robotics, AI, programming terms) in English
- Maintain the educational tone appropriate for a university-level textbook
- Keep code snippets, mathematical formulas, and proper nouns in English
- Ensure the Urdu translation is grammatically correct and natural-sounding
- Maintain the original structure and formatting as much as possible"""

                # Prepare the user message with the content to translate
                user_message = f"Translate the following content from English to Urdu:\n\n{request.text}"

                print(f"Making API call to Groq with model: {self.model_name}")

                # Make the API call to Groq
                chat_completion = await self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],
                    model=self.model_name,
                    temperature=0.3,  # Lower temperature for more consistent translations
                    max_tokens=8000,  # Adjust based on content length
                )

                # Extract the translated content
                translated_content = chat_completion.choices[0].message.content
                print(f"Received translation of length: {len(translated_content) if translated_content else 0}")

                # Calculate processing time
                processing_time = int((time.time() - start_time) * 1000)

                # Create translation metadata
                metadata = TranslationMetadata(
                    processing_time=processing_time,
                    token_count=len(request.text.split()),  # Simple token count estimation
                    confidence_score=0.95  # High confidence for now, could be calculated based on response quality
                )

                # Create and return the response
                response = TranslationResponse(
                    original_content=request.text,
                    translated_content=translated_content,
                    language_from=request.source_language,
                    language_to=request.target_language,
                    translation_metadata=metadata
                )

                print(f"Translation completed successfully in {processing_time}ms")
                return response

        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            error_msg = f"Translation failed: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)