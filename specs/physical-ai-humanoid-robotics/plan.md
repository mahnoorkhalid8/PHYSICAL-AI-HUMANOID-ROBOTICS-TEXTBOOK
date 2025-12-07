# Implementation Plan: Physical AI Humanoid Robotics Textbook (Docusaurus)

**Branch**: `001-ai-humanoid-robotics-book` | **Date**: 2025-12-05 | **Spec**: C:\Users\SEVEN86 COMPUTES\Physical-AI-Humanoid-Robotics-Textbook\.specify\specs\physical-ai-humanoid-robotics\spec.md
**Input**: Feature specification from `/specs/001-ai-humanoid-robotics-book/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

A comprehensive Docusaurus book source repository for Physical AI Humanoid Robotics, organized under 'humanoid-robotics/docs/', containing four modules, 13 weekly topics, and all necessary technical artifacts for the RAG Chatbot and Agent system. The implementation prioritizes system setup before content generation.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11, JavaScript/React
**Primary Dependencies**: Docusaurus, FastAPI, Qdrant, OpenAI, ROS 2, Gazebo, NVIDIA Isaac, Whisper
**Storage**: Qdrant (vector database), local filesystem (MDX content)
**Testing**: pytest (FastAPI backend), Docusaurus build (frontend), manual verification (agent compliance, RAG integration)
**Target Platform**: Linux server (FastAPI, Qdrant), Web (Docusaurus)
**Project Type**: Web application (Docusaurus frontend, FastAPI backend)
**Performance Goals**: Low latency for RAG chatbot responses (e.g., <500ms p95)
**Constraints**: Docusaurus file structure adherence, MDX content format, Docusaurus linking, code block formatting, agent system integration
**Scale/Scope**: Four modules, 13 weekly topics, RAG chatbot, agent system.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Agent Authority:** All content generation and code changes must be initiated via Spec-Kit Plus commands (e.g., /sp.implement, /sp.spec). (Compliant)
- **Docusaurus Compatibility:** All generated content must be valid MDX (Markdown with React) and organized according to the Docusaurus file structure (humanoid-robotics/docs/). (Compliant)
- **GitHub Readiness:** All code changes must be small, testable, and adhere to conventional commit standards for seamless deployment via GitHub Actions. (Compliant)
- **Accuracy & Rigor:** Technical claims must be accurate, verified, and follow high-quality textbook standards. (Compliant)
- **Content Location:** All book content must be placed within the 'humanoid-robotics/docs/' directory. (Compliant)
- **Code Standards:** All generated code examples (in any language) must be complete, runnable, and use Docusaurus code block format with language specification (e.g., ```typescript). (Compliant)
- **Review Protocol:** Code blocks exceeding 20 lines or architectural changes must be reviewed by the 'code-optimizer' Subagent before final commitment. (To be enforced by agent orchestration)
- **Style:** Writing style must be professional, educational, and accessible to a computer science undergraduate audience. (Compliant, to be enforced by style-reviewer agent)
- **Deployment Target:** Final output must be deployable to GitHub Pages using the Docusaurus build process. (Compliant)
- **Technology Stack:** Content generation must use the Claude Code Router/Gemini models, and deployment must use Docusaurus/GitHub Actions. (Compliant)
- **File Naming:** All document files must use lowercase, hyphenated slugs (e.g., '01-introduction-to-robotics.mdx'). (Compliant)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
humanoid-robotics/
├── docs/
│   ├── 01-robotic-nervous-system/
│   │   ├── 01-foundations-physical-ai.mdx
│   │   ├── 02-ros2-architecture.mdx
│   │   ├── 03-ros2-nodes-topics-services.mdx
│   │   ├── 04-bridging-python-agents-rclpy.mdx
│   │   └── 05-urdf-robot-description.mdx
│   ├── 02-digital-twin-simulation/
│   │   ├── 01-gazebo-simulation-setup.mdx
│   │   ├── 02-urdf-sdf-formats.mdx
│   │   ├── 03-physics-sensor-simulation.mdx
│   │   └── 04-unity-visualization-setup.mdx
│   ├── 03-ai-robot-brain-isaac/
│   │   ├── 01-isaac-sdk-sim-overview.mdx
│   │   ├── 02-perception-manipulation.mdx
│   │   ├── 03-reinforcement-learning-control.mdx
│   │   └── 04-sim-to-real-transfer.mdx
│   └── 04-vision-language-action/
│       ├── 01-gpt-integration-conversational.mdx
│       ├── 02-speech-recognition-whisper.mdx
│       ├── 03-cognitive-planning-llm-to-ros.mdx
│       └── 04-capstone-autonomous-humanoid.mdx
├── src/
│   └── components/
│       └── ChatbotWidget.js
├── docusaurus.config.js
└── package.json

rag-backend/
├── ingest.py
└── main.py

.claude/
└── agents/
    └── style-reviewer.md
```

**Structure Decision**: The project will follow a hybrid structure. The main book content will reside within a Docusaurus project under `humanoid-robotics/`. The RAG chatbot backend will be in a separate `rag-backend/` directory, and the Claude Code agent definitions will be under `.claude/agents/`.

## Phased Implementation

This plan follows three distinct phases:

### Phase 1: System Foundation

*   **Implement RAG Backend Files**:
    *   `rag-backend/ingest.py`: Implement the data ingestion logic for MDX content. This will involve client-side extraction or server-side file reading, and chunking strategies for Qdrant.
    *   `rag-backend/main.py`: Implement the FastAPI backend, including the `/chat` endpoint with the defined RAG API contract (Input: query, selected_text; Output: response, source_url).
*   **Implement Agent System Files**:
    *   `.claude/agents/style-reviewer.md`: Implement the style-reviewer Subagent based on the style guidelines from the Constitution.
*   **Implement Chatbot Widget**:
    *   `humanoid-robotics/src/components/ChatbotWidget.js`: Implement the Docusaurus Chatbot Widget for user interaction with the FastAPI backend.

### Phase 2: Book Structure

*   **Generate Module Directories**: Create the four top-level module directories under `humanoid-robotics/docs/`:
    *   `01-robotic-nervous-system/`
    *   `02-digital-twin-simulation/`
    *   `03-ai-robot-brain-isaac/`
    *   `04-vision-language-action/`
*   **Generate Skeletal MDX Files**: Create the 13 empty or skeletal MDX files within their respective module folders, following the ordered naming convention (e.g., `01-foundations-physical-ai.mdx`).

### Phase 3: Content Generation

*   **Implement Content for 13 Topics**: Populate all 13 MDX files with detailed content, including:
    *   **Code Blocks**: Ensure each technical explanation has at least one syntactically highlighted code block (Python, YAML, C++, URDF, Launch File).
    *   **Cross-Referencing**: Add internal Docusaurus links to related topics across modules.
    *   **Hardware Specifications**: Integrate Markdown tables for "Digital Twin" Workstation and "Physical AI" Edge Kit into `01-foundations-physical-ai.mdx`.
    *   **Artifacts**: Generate specific artifacts as per `spec.md` (ROS 2 Python node example, URDF snippet, SDF snippet, Simulated Sensor Specifications table, Isaac Sim Python script outline, Isaac ROS VSLAM pipeline diagram explanation, LLM to ROS actions Python code block).
*   **Agent Compliance**: Ensure all content adheres to the 'style-reviewer' Subagent guidelines.
