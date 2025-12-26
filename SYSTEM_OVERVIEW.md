# Auth Personalization System - Architecture Overview

## System Components

### 1. Auth Service (`auth-service/`)
- **Port**: 4000
- **Purpose**: Provides authentication and JWT signing functionality
- **Key Features**:
  - JWKS endpoint at `/auth/jwks` for public key distribution
  - User registration with additional fields (software_background, hardware_background)
  - RS256 JWT token generation
- **Technology**: Node.js + Express + jose

### 2. Backend Service (`backend/`)
- **Port**: 8000
- **Purpose**: FastAPI backend for personalization logic
- **Key Features**:
  - `/api/personalize` endpoint for content personalization
  - JWT validation using JWKS from auth service
  - RAG-based content generation using Groq API
  - Integration with Neon DB for user data
- **Technology**: Python + FastAPI + python-jose

### 3. Frontend Service (`frontend/`)
- **Port**: 3000
- **Purpose**: Docusaurus documentation site with personalization
- **Key Features**:
  - PersonalizeButton component for content personalization
  - Auth context for user session management
  - Integration with backend personalization API
  - Signup form with background questions
- **Technology**: React + Docusaurus + TypeScript

## API Flow

### Personalization Flow
1. User clicks "Personalize This Chapter" button
2. Frontend gets user's JWT token from auth service
3. Frontend calls backend `/api/personalize` with JWT in Authorization header
4. Backend validates JWT using JWKS from auth service (http://localhost:4000/auth/jwks)
5. Backend extracts user background from JWT claims
6. Backend generates personalized content using Groq API
7. Backend returns personalized content to frontend
8. Frontend displays personalized content in modal

### Authentication Flow
1. User registers via signup form with background information
2. Auth service creates user account with additional fields
3. Auth service generates JWT with user background claims
4. Frontend stores JWT and user information
5. JWT is attached to all backend API requests

## Environment Configuration

### Auth Service (.env)
```
NEON_DB_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
```

### Backend (.env)
```
GROQ_API_KEY=your-groq-api-key-here
BETTER_AUTH_JWKS_URL=http://localhost:4000/auth/jwks
NEON_DB_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
```

### Frontend (.env)
```
REACT_APP_BETTER_AUTH_URL=http://localhost:4000
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Running the System

1. Start Auth Service: `cd auth-service && npx tsx index.ts`
2. Start Backend: `cd backend && python -m uvicorn main:app --reload --port 8000`
3. Start Frontend: `cd frontend && npm start` (or `npx docusaurus start`)

## Key Endpoints

- Auth Service JWKS: `http://localhost:4000/auth/jwks`
- Backend Health: `http://localhost:8000/health`
- Backend Personalization: `http://localhost:8000/api/personalize`
- Frontend: `http://localhost:3000`

## Database Schema

- Neon DB with users table extended with:
  - `software_background` (string)
  - `hardware_background` (string)
  - Standard Better Auth user fields

## Security

- RS256 JWT algorithm for token signing
- JWKS-based token validation
- Secure token transmission in Authorization header
- User background data protected in JWT claims