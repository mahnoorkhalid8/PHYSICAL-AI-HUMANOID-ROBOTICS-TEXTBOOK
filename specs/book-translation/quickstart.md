# Quickstart Guide: AI-Powered Urdu Translation

**Feature**: Book Translation | **Date**: 2025-12-29

## Overview

This guide provides step-by-step instructions to set up and run the AI-powered Urdu translation feature for the Docusaurus-based robotics textbook.

## Prerequisites

- Node.js 18+ (for frontend/Docusaurus)
- Python 3.11+ (for backend/FastAPI)
- npm or yarn package manager
- Groq API key for translation service
- JWT token configuration for authentication

## Backend Setup (FastAPI)

### 1. Install Backend Dependencies

```bash
cd backend
pip install fastapi uvicorn python-jose[cryptography] groq python-multipart
pip install pytest httpx  # for testing
```

### 2. Environment Configuration

Create a `.env` file in the backend directory:

```env
GROQ_API_KEY=your_groq_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=RS256
JWKS_URL=your_jwks_endpoint_url
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run the Backend Server

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## Frontend Setup (Docusaurus)

### 1. Install Frontend Dependencies

```bash
cd frontend  # or root directory if Docusaurus is in root
npm install
```

### 2. Environment Configuration

Add to your `.env` file:

```env
REACT_APP_TRANSLATION_API_URL=http://localhost:8000/api
REACT_APP_JWT_AUTH_REQUIRED=true
```

### 3. Run the Frontend

```bash
npm run start
```

## API Usage

### Translation Endpoint

```bash
POST /api/translate
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "content": "Your English content to translate",
  "preserve_technical_terms": true
}
```

### Example Response

```json
{
  "original_content": "Your English content to translate",
  "translated_content": "آپ کا انگریزی مواد ترجمہ کے لیے",
  "language_from": "en",
  "language_to": "ur",
  "translation_metadata": {
    "processing_time": 1250,
    "token_count": 150,
    "confidence_score": 0.92
  }
}
```

## Integration with Docusaurus

### 1. Add TranslateButton Component

The `TranslateButton` component can be integrated into Docusaurus layouts by:

1. Adding the component import to your layout file
2. Placing the component in the appropriate location (e.g., at the top of document pages)
3. Ensuring it only renders for authenticated users

### 2. Content Extraction

The component will automatically extract content from the current Docusaurus page using DOM traversal to target the main content area.

## Development Workflow

### Running Both Servers

For development, you'll typically run both servers simultaneously:

Terminal 1 (Backend):
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
npm run start
```

### Testing

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
npm run test
```

## Troubleshooting

### Common Issues

1. **JWT Authentication Errors**: Ensure your JWT token is properly formatted and not expired
2. **CORS Issues**: Make sure your backend allows requests from your frontend origin
3. **API Key Issues**: Verify your Groq API key is correct and has sufficient quota
4. **Content Extraction Issues**: Check that the component is placed correctly in the Docusaurus layout

### Debugging Tips

- Check browser console for frontend errors
- Check backend logs for API errors
- Verify environment variables are properly set
- Test the API endpoint directly using curl or Postman