# Implementation Plan: Auth Personalization

**Branch**: `1-auth-personalization` | **Date**: 2025-12-25 | **Spec**: [link to system-spec.md](../auth-personalization/system-spec.md)
**Input**: Feature specification from `/specs/auth-personalization/system-spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a personalized authentication system that allows users to register with software and hardware background information, and provides personalized chapter summaries based on their skillset. The system will include:

1. Better Auth configuration to extend the User schema with software_background and hardware_background fields
2. Docusaurus frontend implementation of a PersonalizeButton component using MDX and a useAuth hook
3. FastAPI backend with a new /api/personalize endpoint that validates RS256 JWT via JWKS URL and performs RAG-based personalization logic
4. State management solution for displaying personalized text to the user (modal or injected div)

## Technical Context

**Language/Version**: TypeScript/JavaScript for frontend, Python 3.11 for backend
**Primary Dependencies**: Better Auth, Docusaurus, FastAPI, Neon DB, Groq API/Qwen
**Storage**: Neon DB for user data storage
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (frontend + backend)
**Project Type**: Web
**Performance Goals**: 95% of personalization requests return within acceptable response time
**Constraints**: Must use RS256 algorithm for JWT validation, secure token verification for backend services
**Scale/Scope**: Support for authenticated users with background information

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Agent Authority:** All content generation and code changes must be initiated via Spec-Kit Plus commands (e.g., /sp.implement, /sp.spec).
*   **Docusaurus Compatibility:** All generated content must be valid MDX (Markdown with React) and organized according to the Docusaurus file structure (humanoid-robotics/docs/).
*   **GitHub Readiness:** All code changes must be small, testable, and adhere to conventional commit standards for seamless deployment via GitHub Actions.
*   **Accuracy & Rigor:** Technical claims must be accurate, verified, and follow high-quality textbook standards.

## Project Structure

### Documentation (this feature)

```text
specs/auth-personalization/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── services/
│   └── hooks/
└── tests/
```

**Structure Decision**: Web application with separate backend (FastAPI) and frontend (Docusaurus) components to handle authentication and personalization features.

## Implementation Details

### 1. Better Auth Configuration

**Objective**: Extend the User schema with software_background and hardware_background fields

**Approach**:
- Configure Better Auth with additional fields for user registration
- Store software_background and hardware_background in the User profile using additional fields capability
- Implement validation for these fields during registration
- Ensure fields are accessible in JWT tokens for backend verification

**Files to create/update**:
- `backend/src/auth/config.ts` - Better Auth configuration with additional fields
- `backend/src/auth/schemas.ts` - Extended user schema definition

### 2. Docusaurus Frontend Implementation

**Objective**: Create a PersonalizeButton component using MDX and a useAuth hook

**Approach**:
- Create a reusable PersonalizeButton React component
- Implement useAuth hook to handle authentication state
- Integrate the component into Docusaurus MDX pages
- Add UI state management for loading, success, and error states
- Ensure the button appears at the top of every documentation page

**Files to create/update**:
- `frontend/src/components/PersonalizeButton/PersonalizeButton.tsx` - Main button component
- `frontend/src/components/PersonalizeButton/useAuth.ts` - Authentication hook
- `frontend/src/components/PersonalizeButton/styles.css` - Component styling

### 3. FastAPI Backend Implementation

**Objective**: Create a new /api/personalize endpoint that validates RS256 JWT via JWKS URL and performs RAG-based personalization logic

**Approach**:
- Implement JWT validation middleware using RS256 algorithm and JWKS
- Create /api/personalize endpoint that accepts chapter content and user background
- Integrate with Groq API/Qwen for AI-powered content generation
- Implement RAG (Retrieval-Augmented Generation) logic for personalization
- Add proper error handling and response formatting

**Files to create/update**:
- `backend/src/api/personalize.py` - Personalization endpoint
- `backend/src/auth/jwt_validator.py` - JWT validation utilities
- `backend/src/services/personalization_service.py` - RAG and AI integration
- `backend/src/models/personalization.py` - Request/response models

### 4. State Management

**Objective**: Implement solution for displaying personalized text to the user (modal or injected div)

**Approach**:
- Create state management for personalization responses
- Implement modal component for displaying personalized content
- Add loading and error states
- Ensure responsive design and accessibility
- Provide option to close/dismiss personalized content

**Files to create/update**:
- `frontend/src/components/PersonalizeModal/PersonalizeModal.tsx` - Modal component
- `frontend/src/components/PersonalizeButton/usePersonalization.ts` - State management hook

## Phase 0: Research & Analysis

### Research Tasks

1. **Better Auth Schema Extension**
   - Research how to extend Better Auth user schema with additional fields
   - Investigate JWT token customization options
   - Review Neon DB integration patterns

2. **Docusaurus Component Integration**
   - Research MDX component integration in Docusaurus
   - Investigate authentication hook patterns
   - Review Docusaurus plugin architecture for global components

3. **JWT Validation with RS256 & JWKS**
   - Research FastAPI JWT validation with RS256 algorithm
   - Investigate JWKS endpoint integration patterns
   - Review security best practices

4. **RAG Implementation with AI Services**
   - Research Groq API/Qwen integration patterns
   - Investigate RAG architecture for content personalization
   - Review prompt engineering for personalized summaries

## Phase 1: Design & Architecture

### Data Model Design
- User profile schema with extended fields
- Personalization request/response models
- Authentication token structure

### API Contract Design
- /api/personalize endpoint specification
- Request/response schemas
- Error handling patterns
- Authentication requirements

### Frontend Architecture
- Component hierarchy for personalization features
- State management patterns
- Authentication flow integration

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|