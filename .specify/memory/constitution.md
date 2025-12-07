<!-- Sync Impact Report -->
<!--
Version change: 0.0.0 -> 1.0.0 (MINOR: Initial constitution creation)
Modified principles: None (initial creation)
Added sections: Core Principles, Key Standards, Constraints, Governance
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ updated
- .specify/templates/spec-template.md: ✅ updated
- .specify/templates/tasks-template.md: ✅ updated
- .specify/templates/commands/sp.constitution.md: ✅ updated
Follow-up TODOs:
- TODO(Documentation): The "Documentation" success criterion in the user's prompt was truncated. This needs clarification.
-->
# AI/Spec-Driven Book: Humanoid Robotics Textbook (Docusaurus) Constitution

## Core Principles

### Agent Authority
All content generation and code changes must be initiated via Spec-Kit Plus commands (e.g., /sp.implement, /sp.spec).

### Docusaurus Compatibility
All generated content must be valid MDX (Markdown with React) and organized according to the Docusaurus file structure (humanoid-robotics/docs/).

### GitHub Readiness
All code changes must be small, testable, and adhere to conventional commit standards for seamless deployment via GitHub Actions.

### Accuracy & Rigor
Technical claims must be accurate, verified, and follow high-quality textbook standards.

## Key Standards

Content Location: All book content must be placed within the 'humanoid-robotics/docs/' directory.
Code Standards: All generated code examples (in any language) must be complete, runnable, and use Docusaurus code block format with language specification (e.g., ```typescript).
Review Protocol: Code blocks exceeding 20 lines or architectural changes must be reviewed by the 'code-optimizer' Subagent before final commitment.
Style: Writing style must be professional, educational, and accessible to a computer science undergraduate audience.

## Constraints

Deployment Target: Final output must be deployable to GitHub Pages using the Docusaurus build process.
Technology Stack: Content generation must use the Claude Code Router/Gemini models, and deployment must use Docusaurus/GitHub Actions.
File Naming: All document files must use lowercase, hyphenated slugs (e.g., '01-introduction-to-robotics.mdx').

## Governance

Build Success: The Docusaurus `npm run build` command must execute with zero errors.
Agent Compliance: Zero deviations from the `/sp.` workflow; all changes justified and traceable.
Documentation: All generated features, code examples, and arch

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
