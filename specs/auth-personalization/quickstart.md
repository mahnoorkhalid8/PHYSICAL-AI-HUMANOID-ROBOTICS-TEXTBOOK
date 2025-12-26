# Quickstart Guide: Auth Personalization Feature

## Overview
This guide provides a quick setup for the personalized authentication system that allows users to register with software and hardware background information, and provides personalized chapter summaries based on their skillset.

## Prerequisites
- Node.js 18+ for frontend (Docusaurus)
- Python 3.11+ for backend (FastAPI)
- Better Auth account/configured instance
- Groq API key for AI services
- Neon DB account/instance

## Frontend Setup (Docusaurus)

### 1. Install Dependencies
```bash
cd frontend
npm install @better-auth/react @better-auth/client
```

### 2. Add PersonalizeButton Component
```bash
# Create the component directory
mkdir -p src/components/PersonalizeButton
```

### 3. Environment Variables
Add to your `.env` file:
```
REACT_APP_BETTER_AUTH_URL=your-better-auth-instance-url
REACT_APP_API_BASE_URL=your-backend-api-url
```

## Backend Setup (FastAPI)

### 1. Install Dependencies
```bash
pip install fastapi python-jose[cryptography] python-multipart better-auth groq
```

### 2. Environment Variables
Add to your `.env` file:
```
GROQ_API_KEY=your-groq-api-key
BETTER_AUTH_JWKS_URL=your-better-auth-jwks-url
NEON_DB_URL=your-neon-db-connection-string
```

### 3. Run the Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

## Integration Steps

### 1. Better Auth Configuration
1. Configure additional fields in Better Auth:
   - Add `software_background` field
   - Add `hardware_background` field
   - Ensure these are included in JWT tokens

### 2. Docusaurus Integration
1. Add the PersonalizeButton component to your MDX pages:
```mdx
import PersonalizeButton from '@site/src/components/PersonalizeButton';

<PersonalizeButton chapterContent={/* chapter content */} />
```

### 3. Frontend-Backend Connection
1. The PersonalizeButton will make requests to `/api/personalize`
2. JWT token is automatically attached to requests
3. Personalized content is displayed in a modal

## Running the Full System

### 1. Start Backend
```bash
cd backend
uvicorn main:app --reload
```

### 2. Start Frontend
```bash
cd frontend
npm start
```

### 3. Access the System
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Testing the Feature

### 1. User Registration
1. Visit the registration page
2. Fill in email, password, and both background fields
3. Verify account creation with extended user profile

### 2. Personalization Flow
1. Navigate to any documentation page
2. Click the "Personalize This Chapter" button
3. View the AI-generated personalized content in the modal
4. Verify content is tailored to your background

## Key Endpoints

### Backend API
- `POST /api/personalize` - Generate personalized content
- `GET /auth/jwks` - JWT validation keys (from Better Auth)

### Frontend Components
- `PersonalizeButton.tsx` - Main button component
- `useAuth.ts` - Authentication hook
- `PersonalizeModal.tsx` - Modal for displaying personalized content

## Troubleshooting

### Common Issues
1. **JWT Validation Errors**: Verify JWKS URL is correct and accessible
2. **API Connection Issues**: Check backend URL in frontend environment variables
3. **Component Not Loading**: Verify all dependencies are installed

### Debugging
- Enable debug logging in backend for API calls
- Check browser console for frontend errors
- Verify environment variables are set correctly