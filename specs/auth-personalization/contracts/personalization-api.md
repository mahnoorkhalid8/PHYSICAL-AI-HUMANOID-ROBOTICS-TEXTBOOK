# API Contract: Personalization Service

## Endpoint: POST /api/personalize

### Description
Generates personalized content based on user background and chapter content. This endpoint accepts the chapter content and user information, then returns a personalized summary tailored to the user's skill level.

### Request

#### Headers
```
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
```

#### Body
```json
{
  "chapter_content": "string (required) - The full content of the chapter to personalize",
  "chapter_title": "string (optional) - The title of the chapter",
  "user_id": "string (required) - The authenticated user's ID",
  "user_background": {
    "software": "string (required) - User's software background",
    "hardware": "string (required) - User's hardware background"
  }
}
```

### Response

#### Success Response (200 OK)
```json
{
  "id": "string - Unique identifier for this personalization response",
  "personalized_content": "string - The AI-generated personalized content",
  "personalization_reasoning": "string - Brief explanation of personalization approach",
  "generated_at": "string - ISO 8601 timestamp of generation",
  "processing_time_ms": "integer - Time taken to process the request in milliseconds"
}
```

#### Error Responses

**400 Bad Request**
```json
{
  "error": "string - Error message describing the issue",
  "details": "object - Additional error details if applicable"
}
```

**401 Unauthorized**
```json
{
  "error": "string - 'Unauthorized' or specific auth error message"
}
```

**403 Forbidden**
```json
{
  "error": "string - 'Forbidden' or specific permission error message"
}
```

**429 Too Many Requests**
```json
{
  "error": "string - 'Rate limit exceeded'",
  "retry_after": "integer - Seconds to wait before retrying"
}
```

**500 Internal Server Error**
```json
{
  "error": "string - 'Internal server error'"
}
```

### Authentication
- JWT token must be provided in Authorization header
- Token must be valid and not expired
- User must be authenticated to access this endpoint

### Validation Rules
- `chapter_content` must not be empty (min 10 characters)
- `user_background` fields must not be empty
- `user_id` must match the authenticated user
- Content must be in plain text format (no HTML/Markdown)

### Rate Limiting
- Maximum 10 requests per user per minute
- Excessive requests will result in 429 responses

### Examples

#### Request Example
```json
{
  "chapter_content": "This chapter covers the fundamentals of humanoid robotics, including kinematics, dynamics, and control systems. We'll explore how to model the movement of robotic limbs and how to control them effectively.",
  "chapter_title": "Introduction to Humanoid Robotics",
  "user_id": "user-12345",
  "user_background": {
    "software": "Intermediate Python developer with robotics experience",
    "hardware": "Basic understanding of electronic circuits"
  }
}
```

#### Response Example
```json
{
  "id": "personalize-67890",
  "personalized_content": "Since you have intermediate Python experience with robotics, we'll focus on the software implementation aspects of humanoid kinematics. The control algorithms will be presented with Python code examples that build on your existing knowledge...",
  "personalization_reasoning": "Content adapted based on user's intermediate Python skills and robotics experience to provide more technical depth",
  "generated_at": "2025-12-25T10:30:00Z",
  "processing_time_ms": 1250
}
```