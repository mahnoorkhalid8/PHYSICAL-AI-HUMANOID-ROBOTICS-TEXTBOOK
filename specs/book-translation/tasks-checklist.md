# Atomic Tasks: AI-Powered Urdu Translation Implementation

**Feature**: Book Translation | **Date**: 2025-12-29

## Frontend Tasks

### Task 1: Create UI Button Component
- [ ] Create `TranslateButton` React component
- [ ] Add proper styling and positioning at start of Docusaurus documents
- [ ] Implement loading state spinner
- [ ] Add accessibility attributes and ARIA labels
- [ ] Create associated CSS styles for the button

### Task 2: Create Translation Result Modal/Container
- [ ] Create `TranslationResult` component to display translated content
- [ ] Implement side-by-side view layout option
- [ ] Implement overlay/toggle view layout option
- [ ] Add proper styling for Urdu text rendering
- [ ] Include controls to switch between original and translated views

### Task 3: Hook into Better Auth State
- [ ] Import Better Auth client in the translation component
- [ ] Check authentication status before showing translation button
- [ ] Implement logic to hide/show button based on auth state
- [ ] Add proper error handling for authentication failures
- [ ] Test button visibility with both authenticated and non-authenticated users

## Backend Tasks

### Task 4: Implement /api/translate Route
- [ ] Create FastAPI endpoint at `/api/translate`
- [ ] Define request/response models for translation
- [ ] Add proper error handling and validation
- [ ] Implement rate limiting to prevent abuse
- [ ] Add logging for monitoring and debugging

### Task 5: Implement JWT Verification
- [ ] Create JWT verification middleware
- [ ] Verify RS256 JWT tokens using existing JWKS configuration
- [ ] Extract user information from token claims
- [ ] Return 401 error for invalid/missing tokens
- [ ] Test with valid and invalid JWT tokens

### Task 6: Add Groq Client Logic
- [ ] Install and configure Groq client library
- [ ] Create translation service function
- [ ] Implement system prompt for Urdu translation
- [ ] Add logic to preserve technical terms in English
- [ ] Handle API errors and timeouts gracefully

## Integration Tasks

### Task 7: Connect Button Click to API
- [ ] Add click handler to TranslateButton component
- [ ] Extract document content when button is clicked
- [ ] Send content to backend API with JWT token
- [ ] Handle loading state during translation
- [ ] Test API connection with mock data

### Task 8: Handle API Response
- [ ] Process successful translation responses
- [ ] Display translated content in the result modal/container
- [ ] Handle error responses appropriately
- [ ] Add error messages for various failure scenarios
- [ ] Implement retry logic for failed requests

### Task 9: Content Extraction Logic
- [ ] Create utility function to extract document content from Docusaurus pages
- [ ] Preserve document structure while extracting text
- [ ] Handle different content types (text, code blocks, etc.)
- [ ] Test extraction on various document layouts
- [ ] Optimize for performance with large documents

## Testing Tasks

### Task 10: Frontend Testing
- [ ] Write unit tests for TranslateButton component
- [ ] Write unit tests for TranslationResult component
- [ ] Test authentication state handling
- [ ] Test content extraction functionality
- [ ] Test UI state transitions (loading, success, error)

### Task 11: Backend Testing
- [ ] Write unit tests for JWT verification
- [ ] Write unit tests for translation endpoint
- [ ] Test API error handling
- [ ] Test rate limiting functionality
- [ ] Test with various content sizes

## Deployment Tasks

### Task 12: Environment Configuration
- [ ] Add environment variables for Groq API key
- [ ] Configure JWT settings in environment
- [ ] Set up proper CORS configuration
- [ ] Configure production vs development settings
- [ ] Document environment variable requirements

### Task 13: Integration Testing
- [ ] Test complete flow from button click to translation display
- [ ] Test with various document types and sizes
- [ ] Test authentication flow integration
- [ ] Test error handling end-to-end
- [ ] Verify performance with realistic content sizes