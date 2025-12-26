# Data Model: Auth Personalization

## User Profile Schema

### Extended User Model
```typescript
interface User {
  id: string;              // Unique identifier (UUID)
  email: string;           // User's email address (unique, required)
  emailVerified: boolean;  // Whether email has been verified
  name: string;            // User's display name (optional)
  image: string;           // Profile image URL (optional)

  // Extended fields for personalization
  software_background: string;  // User's software background/experience level
  hardware_background: string;  // User's hardware background/experience level

  createdAt: Date;         // Account creation timestamp
  updatedAt: Date;         // Last update timestamp
}
```

### Validation Rules
- `email`: Must be valid email format, unique across system
- `software_background`: Required field during registration, string length 2-100 characters
- `hardware_background`: Required field during registration, string length 2-100 characters
- Both background fields: Must be from predefined options or free text (2-200 characters)

## Personalization Request Model

### Request Schema
```typescript
interface PersonalizationRequest {
  chapterContent: string;    // The content of the chapter to personalize
  chapterTitle?: string;     // Title of the chapter (optional)
  userId: string;            // ID of the authenticated user
  userBackground: {
    software: string;        // User's software background
    hardware: string;        // User's hardware background
  };
}
```

### Response Schema
```typescript
interface PersonalizationResponse {
  id: string;                // Unique response identifier
  originalChapterId?: string; // Reference to original chapter (if applicable)
  personalizedContent: string; // The AI-generated personalized content
  personalizationReasoning: string; // Brief explanation of personalization approach
  generatedAt: Date;         // Timestamp of generation
  processingTimeMs: number;  // Time taken to process the request
}
```

## Authentication Token Model

### JWT Claims
```typescript
interface AuthToken {
  // Standard JWT claims
  sub: string;               // Subject (user ID)
  iat: number;               // Issued at timestamp
  exp: number;               // Expiration timestamp
  nbf: number;               // Not before timestamp

  // Custom claims for personalization
  user_metadata: {
    email: string;
    name?: string;
    software_background: string;
    hardware_background: string;
  };
}
```

## API Request/Response Models

### Personalization API Request
```python
from pydantic import BaseModel
from typing import Optional

class PersonalizeRequest(BaseModel):
    chapter_content: str
    chapter_title: Optional[str] = None
    user_id: str
    user_background: dict

class PersonalizeResponse(BaseModel):
    id: str
    personalized_content: str
    personalization_reasoning: str
    generated_at: str
    processing_time_ms: int
```

## Database Schema (Neon DB)

### User Table Extension
```sql
-- This extends the existing Better Auth user table
-- Additional columns added to the users table
ALTER TABLE users
ADD COLUMN software_background VARCHAR(200) NOT NULL,
ADD COLUMN hardware_background VARCHAR(200) NOT NULL;
```

## State Management Models (Frontend)

### Personalization State
```typescript
type PersonalizationState = {
  status: 'idle' | 'loading' | 'success' | 'error';
  personalizedContent: string | null;
  error: string | null;
  processingTime: number | null;
  modalVisible: boolean;
};

type PersonalizationAction =
  | { type: 'START_REQUEST' }
  | { type: 'REQUEST_SUCCESS'; payload: PersonalizationResponse }
  | { type: 'REQUEST_ERROR'; payload: string }
  | { type: 'TOGGLE_MODAL'; visible?: boolean }
  | { type: 'RESET' };
```