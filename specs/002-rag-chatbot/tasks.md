---
description: "Task list for RAG Chatbot implementation"
---

# Tasks: RAG Chatbot for Existing Book

**Input**: Design documents from `/specs/002-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths adjusted based on plan.md structure for web application with React frontend and FastAPI backend

## Constitutional Compliance for Tasks *(mandatory)*

*GATE: All tasks and their execution must comply with the project constitution.*

### Core Principles Impacting Tasks

*   **Agent Authority:** Tasks must be initiated via Spec-Kit Plus commands (e.g., /sp.implement, /sp.spec).
*   **Docusaurus Compatibility:** Content-related tasks must produce valid MDX and follow Docusaurus structure.
*   **GitHub Readiness:** Code-related tasks must produce small, testable changes adhering to conventional commit standards.
*   **Accuracy & Rigor:** Technical claims and code examples in tasks must be accurate and verified.

### Key Standards for Task Execution

*   **Content Location:** All book content tasks must target the 'humanoid-robotics/docs/' directory.
*   **Code Standards:** Code example tasks must ensure completeness, runnability, and Docusaurus code block format.
*   **Review Protocol:** Tasks involving code blocks exceeding 20 lines or architectural changes must include a 'code-optimizer' Subagent review step.
*   **Style:** Writing tasks must adhere to a professional, educational, and accessible style.

### Constraints for Task Execution

*   **Deployment Target:** Tasks must ensure output is deployable to GitHub Pages using Docusaurus build process.
*   **Technology Stack:** Tasks must leverage Claude Code Router/Gemini models and Docusaurus/GitHub Actions.
*   **File Naming:** Document-related tasks must use lowercase, hyphenated slugs (e.g., '01-introduction-to-robotics.mdx).

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure with FastAPI dependencies
- [x] T002 Create frontend project structure with React dependencies for Docusaurus integration
- [x] T003 [P] Configure environment variables and .env file structure
- [x] T004 [P] Setup Qdrant vector database connection configuration
- [x] T005 [P] Setup Neon Postgres connection configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup database schema and migrations framework for Neon Postgres
- [x] T007 [P] Create Qdrant collection for book embeddings
- [x] T008 [P] Setup API routing and middleware structure for FastAPI
- [x] T009 Create base data models for ChatSession and Message entities
- [x] T010 Configure error handling and logging infrastructure
- [x] T011 Setup environment configuration management
- [x] T012 Implement ingestion pipeline to embed book content into Qdrant

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Interactive Book Queries (Priority: P1) 🎯 MVP

**Goal**: Enable students to ask questions about textbook content and receive relevant answers based on book information

**Independent Test**: A student can ask questions about the textbook content and receive relevant answers based on the book's information through an embedded chat interface.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T013 [P] [US1] Contract test for /api/query endpoint in backend/tests/contract/test_query.py
- [x] T014 [P] [US1] Integration test for full-book RAG query in backend/tests/integration/test_rag_query.py

### Implementation for User Story 1

- [x] T015 [P] [US1] Create QueryContext model in backend/src/models/query_context.py
- [x] T016 [P] [US1] Create VectorEmbedding model representation in backend/src/models/vector_embedding.py
- [x] T017 [US1] Implement ChatService in backend/src/services/chat_service.py (depends on T009)
- [x] T018 [US1] Implement RAG query service in backend/src/services/rag_service.py
- [x] T019 [US1] Implement /api/query POST endpoint in backend/src/api/query_endpoint.py
- [x] T020 [US1] Add validation and error handling for query endpoint
- [x] T021 [US1] Create React ChatbotWidget component in src/components/ChatbotWidget.jsx
- [x] T022 [US1] Create MessageBubble component in src/components/MessageBubble.jsx
- [x] T023 [US1] Create MessageInput component in src/components/MessageInput.jsx
- [x] T024 [US1] Create LoadingIndicator component in src/components/LoadingIndicator.jsx
- [x] T025 [US1] Connect frontend fetch POST to /api/query endpoint
- [x] T026 [US1] Display answers in chat window with proper formatting
- [x] T027 [US1] Add auto-scroll functionality on new messages
- [x] T028 [US1] Style components with black-gold theme and responsive design
- [x] T029 [US1] Embed component in relevant MDX pages for testing

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Context-Aware Querying (Priority: P2)

**Goal**: Allow students to ask questions about specific content they're viewing or have selected on the current page, with responses focused on that context

**Independent Test**: A student can select text on a page or focus on the current page content, query the chatbot, and receive responses that are specifically related to the selected or current context.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T030 [P] [US2] Contract test for /api/query with selected_text parameter in backend/tests/contract/test_query_context.py
- [x] T031 [P] [US2] Integration test for selected-text RAG query in backend/tests/integration/test_context_query.py

### Implementation for User Story 2

- [x] T032 [P] [US2] Enhance QueryContext model to handle selected text context in backend/src/models/query_context.py
- [x] T033 [US2] Implement selected text context handling in backend/src/services/rag_service.py
- [x] T034 [US2] Update /api/query endpoint to process selected_text parameter
- [x] T035 [US2] Add text selection handler to ChatbotWidget component in src/components/ChatbotWidget.jsx
- [x] T036 [US2] Implement JavaScript text selection capture functionality
- [x] T037 [US2] Pass selected text context to backend API calls
- [x] T038 [US2] Update response display to show context-aware answers

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Session Management and History (Priority: P2)

**Goal**: Enable students to continue conversations with the chatbot across multiple pages and sessions, maintaining conversation history

**Independent Test**: A student can have a conversation with the chatbot, navigate to different pages, and continue the conversation with access to previous context and responses.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T039 [P] [US3] Contract test for /api/session endpoints in backend/tests/contract/test_session.py
- [x] T040 [P] [US3] Integration test for session management in backend/tests/integration/test_session.py

### Implementation for User Story 3

- [x] T041 [P] [US3] Create SessionService in backend/src/services/session_service.py
- [x] T042 [US3] Implement /api/session POST endpoint in backend/src/api/session_endpoint.py
- [x] T043 [US3] Implement /api/session/{session_id}/messages GET endpoint in backend/src/api/session_endpoint.py
- [x] T044 [US3] Add session management to ChatService in backend/src/services/chat_service.py
- [x] T045 [US3] Update ChatbotWidget to manage session state in src/components/ChatbotWidget.jsx
- [x] T046 [US3] Implement session persistence in frontend component
- [x] T047 [US3] Add session history display functionality

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T048 [P] Documentation updates in docs/
- [ ] T049 Code cleanup and refactoring
- [ ] T050 Performance optimization across all stories
- [ ] T051 [P] Additional unit tests (if requested) in backend/tests/unit/ and frontend/tests/
- [ ] T052 Security hardening for API endpoints
- [ ] T053 Run quickstart.md validation
- [ ] T054 Full integration testing of frontend-backend communication
- [ ] T055 Accessibility compliance testing for chat interface

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for /api/query endpoint in backend/tests/contract/test_query.py"
Task: "Integration test for full-book RAG query in backend/tests/integration/test_rag_query.py"

# Launch all models for User Story 1 together:
Task: "Create QueryContext model in backend/src/models/query_context.py"
Task: "Create VectorEmbedding model representation in backend/src/models/vector_embedding.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence