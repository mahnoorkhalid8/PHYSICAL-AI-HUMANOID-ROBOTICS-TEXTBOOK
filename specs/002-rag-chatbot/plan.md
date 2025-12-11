# Implementation Plan: RAG Chatbot for Existing Book

**Branch**: `002-rag-chatbot` | **Date**: 2025-12-10 | **Spec**: [link to spec.md](../002-rag-chatbot/spec.md)
**Input**: Feature specification from `/specs/[002-rag-chatbot]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a React-based chatbot component embedded in Docusaurus MDX pages that connects to a FastAPI backend for RAG queries. The system uses Qdrant for vector storage of book embeddings and Neon Postgres for session/chat logs, supporting both full-book and selected-text queries with a responsive, accessible black-gold themed UI.

## Technical Context

**Language/Version**: Python 3.11 (FastAPI backend), JavaScript/TypeScript (React frontend)
**Primary Dependencies**: FastAPI, React, Qdrant, Neon Postgres, OpenAI API
**Storage**: Neon Postgres for chat/session storage, Qdrant for vector embeddings
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (Docusaurus integration)
**Project Type**: Web (frontend + backend components)
**Performance Goals**: <3s response time for queries, support 100 concurrent users
**Constraints**: <200ms p95 for UI interactions, REST-based communication, accessible UI
**Scale/Scope**: Single book content, multiple concurrent users, persistent session storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Agent Authority:** All content generation and code changes must be initiated via Spec-Kit Plus commands (e.g., /sp.implement, /sp.spec).
*   **Docusaurus Compatibility:** All generated content must be valid MDX (Markdown with React) and organized according to the Docusaurus file structure (humanoid-robotics/docs/).
*   **GitHub Readiness:** All code changes must be small, testable, and adhere to conventional commit standards for seamless deployment via GitHub Actions.
*   **Accuracy & Rigor:** Technical claims must be accurate, verified, and follow high-quality textbook standards.

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot/
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

# Integration with existing Docusaurus structure
src/
└── components/
    └── ChatbotWidget.jsx    # React component for embedding in MDX
```

**Structure Decision**: Web application structure with separate backend and frontend components, with the React chatbot component integrated into the existing Docusaurus structure through a custom component.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |