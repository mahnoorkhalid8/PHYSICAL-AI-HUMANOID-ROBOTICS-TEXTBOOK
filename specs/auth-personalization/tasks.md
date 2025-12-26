---
description: "Task list for auth-personalization feature implementation"
---

# Tasks: Auth Personalization

**Input**: Design documents from `/specs/auth-personalization/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit test requirements in feature specification, so tests are omitted from this task list.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths based on plan.md structure

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

- [x] T001 Create backend directory structure: backend/src/{models,services,api,auth}
- [x] T002 Create frontend directory structure: frontend/src/{components,services,hooks}
- [x] T003 [P] Install Better Auth dependencies in backend
- [x] T004 [P] Install FastAPI dependencies in backend
- [x] T005 [P] Install Docusaurus and React dependencies in frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup Better Auth configuration with additional fields in backend/src/auth/config.ts
- [x] T007 Setup database migration for Neon DB to add software_background and hardware_background columns
- [x] T008 [P] Create JWT validation utility in backend/src/auth/jwt_validator.py
- [x] T009 [P] Setup JWKS endpoint integration in backend/src/auth/jwt_validator.py
- [x] T010 Create PersonalizationRequest and PersonalizationResponse models in backend/src/models/personalization.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration with Background Information (Priority: P1) 🎯 MVP

**Goal**: Allow users to register with software and hardware background information that gets stored in the user profile

**Independent Test**: Can register a new user with background information and verify the data is stored correctly in the database

### Implementation for User Story 1

- [x] T011 [P] Create extended user schema in backend/src/auth/schemas.ts with software_background and hardware_background fields
- [x] T012 [P] Update Better Auth configuration to include additional fields validation
- [x] T013 Create signup form UI component with background questions in frontend/src/components/SignupForm.tsx
- [x] T014 Add styling for signup form in frontend/src/components/SignupForm.css
- [ ] T015 Test user registration flow with background information

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Personalize Chapter Content (Priority: P1)

**Goal**: Create a 'Personalize This Chapter' button that sends user background to backend and displays personalized content

**Independent Test**: Can authenticate as a user with background information and click the personalization button to receive customized content

### Implementation for User Story 2

- [x] T016 Create PersonalizeButton React component in frontend/src/components/PersonalizeButton/PersonalizeButton.tsx
- [x] T017 Create useAuth hook for handling authentication state in frontend/src/components/PersonalizeButton/useAuth.ts
- [x] T018 Create usePersonalization hook for state management in frontend/src/components/PersonalizeButton/usePersonalization.ts
- [x] T019 [P] Create PersonalizeModal component in frontend/src/components/PersonalizeModal/PersonalizeModal.tsx
- [x] T020 [P] Add styling for PersonalizeButton in frontend/src/components/PersonalizeButton/styles.css
- [x] T021 Create FastAPI endpoint for personalization in backend/src/api/personalize.py
- [x] T022 Implement RAG-based personalization service in backend/src/services/personalization_service.py
- [ ] T023 Connect button to backend API and handle loading/display state in frontend/src/components/PersonalizeButton/PersonalizeButton.tsx
- [ ] T024 Test personalization flow with authenticated user

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Secure Token Validation (Priority: P2)

**Goal**: Validate JWT tokens using RS256 algorithm and JWKS before processing personalization requests

**Independent Test**: Can make requests with valid and invalid JWT tokens to verify proper authentication and authorization

### Implementation for User Story 3

- [x] T025 [P] Enhance JWT validator with RS256 algorithm support in backend/src/auth/jwt_validator.py
- [x] T026 Add authentication middleware for personalization endpoint in backend/src/api/personalize.py
- [x] T027 Implement error handling for invalid tokens in backend/src/auth/jwt_validator.py
- [ ] T028 Test token validation with valid and invalid JWT tokens

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T029 [P] Add documentation for auth-personalization feature
- [x] T030 Code cleanup and refactoring across all components
- [x] T031 [P] Add environment configuration for API keys and service URLs
- [ ] T032 Run quickstart validation to ensure all components work together
- [ ] T033 Integration testing of full user flow

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 user registration being available
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tasks within a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all components for User Story 2 together:
Task: "Create PersonalizeButton React component in frontend/src/components/PersonalizeButton/PersonalizeButton.tsx"
Task: "Create useAuth hook for handling authentication state in frontend/src/components/PersonalizeButton/useAuth.ts"
Task: "Create usePersonalization hook for state management in frontend/src/components/PersonalizeButton/usePersonalization.ts"
Task: "Create PersonalizeModal component in frontend/src/components/PersonalizeModal/PersonalizeModal.tsx"
Task: "Create FastAPI endpoint for personalization in backend/src/api/personalize.py"
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
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence