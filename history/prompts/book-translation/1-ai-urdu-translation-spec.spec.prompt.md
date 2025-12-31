---
id: 1
title: AI Urdu Translation Spec
stage: spec
date: 2025-12-29
surface: agent
model: Claude Sonnet 4.5
feature: book-translation
branch: main
user: unknown
command: /sp.specify
labels: ["specification", "translation", "ai", "urdu", "docusaurus"]
links:
  spec: specs/book-translation/system-spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/book-translation/system-spec.md
 - specs/book-translation/checklists/requirements.md
tests:
 - none
---

## Prompt

Create a new folder in specs named as book-translation and then create specification in specs/book-translation/system-spec.md for an AI-powered Urdu translation feature.

Goal: Allow logged-in users to translate any chapter into Urdu on-demand using Groq.

Requirements:

Trigger: A 'Translate to Urdu' button at the start of every Docusaurus document.

Access Control: The button should only be visible/functional if the user is logged in via Better Auth.

Backend Flow: The frontend sends the current page's content (Markdown/Text) to a FastAPI endpoint /api/translate.

AI Logic: FastAPI uses the Groq API (Qwen-72B or Llama-3) to translate the text into high-quality Urdu while keeping technical robotics terms in English where appropriate.

Security: The request must include the JWT token. FastAPI must verify the token using the existing RS256/JWKS configuration.

UX: Show a loading spinner during translation and display the Urdu text in a clean, readable 'Translation Mode' overlay or a side-by-side view.

## Response snapshot

Successfully created a specification for an AI-powered Urdu translation feature that allows logged-in users to translate robotics textbook chapters on-demand. Created the required folder structure and comprehensive specification document with user scenarios, functional requirements, and success criteria.

## Outcome

- ✅ Impact: Created complete specification for AI Urdu translation feature with all required sections
- 🧪 Tests: none
- 📁 Files: specs/book-translation/system-spec.md, specs/book-translation/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Specification successfully created with technology-agnostic requirements and clear user scenarios

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh not found, had to use manual template approach
- Graders run and results (PASS/FAIL): PASS - Specification meets all quality criteria
- Prompt variant (if applicable): Standard /sp.specify command
- Next experiment (smallest change to try): Verify if PHR script exists in different location