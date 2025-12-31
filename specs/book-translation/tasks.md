---
description: "Task list for AI-powered Urdu translation feature implementation"
---

# Tasks: AI-Powered Urdu Translation

**Input**: Design documents from `/specs/book-translation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure based on plan.md

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

- [X] T001 Create project structure with backend and frontend directories
- [X] T002 [P] Install FastAPI dependencies in backend/requirements.txt
- [X] T003 [P] Install Docusaurus dependencies in frontend/package.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Setup JWT verification middleware in backend/src/auth/
- [X] T005 [P] Configure Groq API client in backend/src/services/
- [X] T006 [P] Setup API routing structure in backend/src/api/
- [X] T007 Create base models for translation in backend/src/models/
- [X] T008 Configure error handling and logging infrastructure
- [X] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Translate Content to Urdu (Priority: P1) 🎯 MVP

**Goal**: Allow logged-in users to translate any chapter of the robotics textbook into Urdu so that they can better understand the content in their native language while preserving technical terminology in English.

**Independent Test**: Can be fully tested by clicking the 'Translate to Urdu' button on any document and verifying that the content is accurately translated and displayed in a readable format.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for /api/translate endpoint in backend/tests/contract/test_translation.py
- [ ] T011 [P] [US1] Integration test for translation flow in backend/tests/integration/test_translation_flow.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Create TranslationRequest model in backend/src/models/translation.py
- [X] T013 [P] [US1] Create TranslationResponse model in backend/src/models/translation.py
- [X] T014 [US1] Implement translation service in backend/src/services/translation_service.py
- [X] T015 [US1] Implement /api/translate endpoint in backend/src/api/v1/translation.py
- [X] T016 [US1] Add JWT verification to translation endpoint
- [X] T017 [US1] Add proper error handling for translation requests

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Frontend Integration (Priority: P2)

**Goal**: Create the UI components and integrate with the translation backend.

**Independent Test**: Can be tested by adding the TranslateButton to a Docusaurus page and verifying it connects to the backend API.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Unit test for TranslateButton component in frontend/tests/components/TranslateButton.test.js
- [ ] T019 [P] [US2] Integration test for translation API call in frontend/tests/integration/translation.test.js

### Implementation for User Story 2

- [X] T020 [P] [US2] Create TranslateButton component in frontend/src/components/TranslateButton/
- [X] T021 [P] [US2] Create TranslationResult component in frontend/src/components/TranslateButton/
- [X] T022 [US2] Implement content extraction utility in frontend/src/utils/contentExtractor.js
- [X] T023 [US2] Add translation state management hook in frontend/src/hooks/useTranslation.js
- [X] T024 [US2] Connect button click to API call with proper error handling
- [X] T025 [US2] Implement loading states and UI feedback

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Authentication Integration (Priority: P3)

**Goal**: Ensure translation functionality is properly protected with Better Auth.

**Independent Test**: Can be tested by attempting to access translation features as both authenticated and non-authenticated users.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US3] Integration test for auth protection in frontend/tests/integration/auth.test.js
- [ ] T027 [P] [US3] Contract test for auth middleware in backend/tests/contract/test_auth.py

### Implementation for User Story 3

- [X] T028 [P] [US3] Hook into Better Auth state in TranslateButton component
- [X] T029 [US3] Implement logic to show/hide translation button based on auth status
- [X] T030 [US3] Add proper error handling for authentication failures
- [X] T031 [US3] Test button visibility with both authenticated and non-authenticated users

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Advanced UI Features (Priority: P4)

**Goal**: Enhance the translation UI with advanced features like side-by-side view and toggle functionality.

**Independent Test**: Can be tested by using the translation feature and verifying the UI correctly toggles between English and Urdu views.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T032 [P] [US4] Unit test for view toggle functionality in frontend/tests/components/TranslationResult.test.js
- [ ] T033 [P] [US4] Integration test for state management in frontend/tests/integration/state.test.js

### Implementation for User Story 4

- [X] T034 [P] [US4] Implement side-by-side view layout in TranslationResult component
- [X] T035 [US4] Add toggle functionality between original and translated views
- [X] T036 [US4] Implement proper styling for Urdu text rendering
- [X] T037 [US4] Add controls to switch between original and translated views
- [X] T038 [US4] Preserve scroll position when toggling views

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T039 [P] Documentation updates in docs/
- [X] T040 Code cleanup and refactoring
- [X] T041 Performance optimization across all stories
- [X] T042 [P] Additional unit tests (if requested) in tests/unit/
- [X] T043 Security hardening
- [X] T044 Run quickstart.md validation

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
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Builds on US2 but should be independently testable

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
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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