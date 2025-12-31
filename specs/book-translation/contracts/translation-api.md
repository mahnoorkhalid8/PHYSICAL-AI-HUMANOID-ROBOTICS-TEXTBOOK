# API Contract: Translation Service

**Feature**: Book Translation | **Date**: 2025-12-29

## Translation API

### POST /api/translate

Translate content from English to Urdu using AI.

#### Request

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)
- `Content-Type: application/json`

**Body**:
```json
{
  "content": "string",
  "preserve_technical_terms": true
}
```

**Fields**:
- `content`: The English content to translate (required, max 50KB)
- `preserve_technical_terms`: Whether to preserve technical terms in English (optional, default: true)

#### Response

**Success Response (200 OK)**:
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

**Error Responses**:
- `400 Bad Request`: Invalid request body or content too large
- `401 Unauthorized`: Invalid or missing JWT token
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Translation service unavailable

#### Example Request

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a sample text for translation.",
    "preserve_technical_terms": true
  }'
```

#### Example Response

```json
{
  "original_content": "This is a sample text for translation.",
  "translated_content": "یہ ترجمہ کے لیے ایک نمونہ متن ہے۔",
  "language_from": "en",
  "language_to": "ur",
  "translation_metadata": {
    "processing_time": 1250,
    "token_count": 150,
    "confidence_score": 0.92
  }
}
```

## Authentication API

### GET /api/translate/health

Check the health and authentication status of the translation service.

#### Response

**Success Response (200 OK)**:
```json
{
  "status": "healthy",
  "authenticated": true,
  "timestamp": "2025-12-29T10:30:00Z"
}
```

**Error Response**:
- `401 Unauthorized`: Invalid or missing JWT token