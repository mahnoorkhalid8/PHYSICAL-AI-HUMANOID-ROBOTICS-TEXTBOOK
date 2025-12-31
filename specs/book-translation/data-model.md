# Data Model: AI-Powered Urdu Translation

**Feature**: Book Translation | **Date**: 2025-12-29

## Core Entities

### TranslationRequest
Represents a user's request to translate content

**Fields**:
- `content` (string): The original English content to be translated
- `user_id` (string): Identifier of the authenticated user
- `language_from` (string): Source language (default: "en")
- `language_to` (string): Target language (default: "ur")
- `preserve_technical_terms` (boolean): Whether to preserve technical terms in English (default: true)
- `timestamp` (datetime): When the request was made

**Validation Rules**:
- Content must not exceed 50KB
- Content must not be empty
- Language codes must be valid ISO 639-1 codes
- User must be authenticated

### TranslationResponse
Represents the translated content response

**Fields**:
- `original_content` (string): The original English content
- `translated_content` (string): The translated Urdu content
- `language_from` (string): Source language (default: "en")
- `language_to` (string): Target language (default: "ur")
- `translation_metadata` (object): Additional information about the translation
  - `processing_time` (number): Time taken for translation in milliseconds
  - `token_count` (number): Number of tokens in the content
  - `confidence_score` (number): Confidence level of the translation (0-1)

**Validation Rules**:
- Translated content must not be empty
- Processing time must be a positive number
- Confidence score must be between 0 and 1

### TranslationSession
Represents the state of a translation session in the UI

**Fields**:
- `session_id` (string): Unique identifier for the session
- `original_content` (string): The original content being translated
- `translated_content` (string): Cached translated content (if available)
- `is_translating` (boolean): Whether translation is in progress
- `translation_error` (string): Error message if translation failed
- `view_mode` (enum): Current view mode ("original", "translated", "side-by-side")
- `timestamp` (datetime): When the session was created

**Validation Rules**:
- Session ID must be unique
- View mode must be one of the allowed values
- If translation_error is present, translated_content must be null

## API Contracts

### POST /api/translate
**Request Body** (`TranslationRequest`):
```json
{
  "content": "string",
  "preserve_technical_terms": true
}
```

**Response** (`TranslationResponse`):
```json
{
  "original_content": "string",
  "translated_content": "string",
  "language_from": "en",
  "language_to": "ur",
  "translation_metadata": {
    "processing_time": 1250,
    "token_count": 150,
    "confidence_score": 0.92
  }
}
```

**Authentication**: JWT token in Authorization header
**Error Responses**:
- 401: Unauthorized (invalid/missing JWT token)
- 400: Bad Request (invalid content, content too large)
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error (translation service unavailable)

## State Transitions

### TranslationSession State Machine
```
[Initial] -> [Content Extracted] -> [Translation Requested] -> [Translating]
    -> [Translation Success] / [Translation Error]
```

**States**:
- `Initial`: No content has been extracted yet
- `Content Extracted`: Document content has been extracted and is ready for translation
- `Translation Requested`: User has clicked translate button, request is being sent
- `Translating`: Translation is in progress, waiting for response
- `Translation Success`: Translation completed successfully
- `Translation Error`: Translation failed due to an error

## Relationships

- `TranslationRequest` is associated with an authenticated `User` (via JWT token)
- `TranslationResponse` is the result of a successful `TranslationRequest`
- `TranslationSession` contains both `TranslationRequest` and `TranslationResponse` data for UI state management