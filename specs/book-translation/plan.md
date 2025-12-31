# Implementation Plan: AI-Powered Urdu Translation

**Branch**: `1-book-translation` | **Date**: 2025-12-29 | **Spec**: [specs/book-translation/system-spec.md](specs/book-translation/system-spec.md)
**Input**: Feature specification from `/specs/book-translation/system-spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an AI-powered Urdu translation feature that allows logged-in users to translate Docusaurus document content on-demand using Groq AI. The solution includes a frontend TranslateButton component that extracts document content, sends it to a backend translation service, and displays the translated Urdu content with preserved technical terms in English.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/React (frontend)
**Primary Dependencies**: FastAPI (backend), Docusaurus/React (frontend), Groq API client
**Storage**: N/A (stateless translation service)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web (Docusaurus documentation site)
**Project Type**: Web (frontend + backend integration)
**Performance Goals**: <30 seconds for translation completion
**Constraints**: <200ms UI response time, JWT authentication required, API rate limits respected
**Scale/Scope**: 100 concurrent translation requests, various document sizes up to 50KB

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Agent Authority:** ✅ All content generation and code changes must be initiated via Spec-Kit Plus commands (e.g., /sp.implement, /sp.spec).
*   **Docusaurus Compatibility:** ✅ All generated content must be valid MDX (Markdown with React) and organized according to the Docusaurus file structure (humanoid-robotics/docs/).
*   **GitHub Readiness:** ✅ All code changes must be small, testable, and adhere to conventional commit standards for seamless deployment via GitHub Actions.
*   **Accuracy & Rigor:** ✅ Technical claims must be accurate, verified, and follow high-quality textbook standards.

## Phase 1 Completion Summary

**Completed Artifacts**:
- `research.md`: Addressed all focus areas (frontend, backend, prompt engineering, state management)
- `data-model.md`: Defined all required data structures and API contracts
- `quickstart.md`: Provided comprehensive setup and usage instructions
- `contracts/translation-api.md`: Specified API contracts for translation service

## Project Structure

### Documentation (this feature)

```text
specs/book-translation/
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
│   │   └── translation.py          # Translation request/response models
│   ├── services/
│   │   └── translation_service.py  # Core translation logic
│   ├── api/
│   │   └── v1/
│   │       └── translation.py      # /api/translate endpoint
│   └── main.py                     # FastAPI app
└── tests/

frontend/
├── src/
│   ├── components/
│   │   └── TranslateButton/        # TranslateButton component
│   ├── hooks/
│   │   └── useTranslation.js       # Translation state management
│   └── utils/
│       └── contentExtractor.js     # Document content extraction
└── tests/
```

**Structure Decision**: Web application with separate backend (FastAPI) and frontend (Docusaurus/React) components to handle translation API and UI respectively.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |