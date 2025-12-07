---
id: 1
title: Relocate Specs Directory and Update Path
stage: general
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch:
user: unknown
command: /sp.implement
labels: ["file-system", "refactoring"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/physical-ai-humanoid-robotics/plan.md
  - .specify/memory/specification-path.md
tests:

---

## Prompt

Task: Relocate the specs directory and update the project's specification path.

1.  **Move Directory:** Use file system tools to move the entire 'specs' directory (and all its contents, including spec.md and plan.md) from the current internal path (.specify/specs/) to the project root directory.
    * FROM: .specify/specs/
    * TO: specs/ (at the project root, next to .specify)

2.  **Update Specification Path Rule:** Create or modify a document in the agent's memory that dictates the new path for specifications.
    * Create file: `.specify/memory/specification-path.md`
    * Content of file: "The authoritative root directory for all Specification artifacts (spec.md, plan.md, tasks.md) is the **specs/** directory, located in the project's root folder, NOT inside .specify/."

3.  **Clean Up:** After the move, ensure the old `.specify/specs/` folder is empty or deleted.

4.  **Verification:** Confirm that the agent can successfully read the relocated 'plan.md' file at the new path: **specs/physical-ai-humanoid-robotics/plan.md**.

## Response snapshot

The `specs` directory was successfully relocated from `.specify/specs/` to the project root `specs/`. A new file `.specify/memory/specification-path.md` was created to define the new specification path. The old `.specify/specs/` directory was removed, and the relocation was verified by reading `specs/physical-ai-humanoid-robotics/plan.md`.

## Outcome

- ✅ Impact: The project's specification directory has been successfully relocated and the new path has been documented.
- 🧪 Tests: The relocation was verified by successfully reading a file from the new path.
- 📁 Files: Moved `specs` directory, created `specification-path.md`.
- 🔁 Next prompts: none
- 🧠 Reflection: The task was completed by moving the directory, creating a documentation file, cleaning up, and verifying the changes.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
