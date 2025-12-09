---
id: 001
title: Move Docusaurus Structure
stage: general
date_iso: 2025-12-09
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: Claude Code
command: /sp.implement
labels: ["docusaurus", "refactor", "typescript", "migration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - package.json
  - package-lock.json
  - docs/
  - src/
  - docusaurus.config.ts
  - sidebars.ts
tests_yaml: []
---

# Move Docusaurus Structure from Subfolder to Root

## User Input

"The goal is to move the entire Docusaurus project structure from the sub-folder, humanoid-robotics, up into the root folder, PHYSICAL-AI-HUMANOID-ROBOTICS-TEXTBOOK, and standardize on TypeScript.

Please execute the following actions in sequence:

Merge Documentation Content: Move the contents (files and sub-folders) of humanoid-robotics/docs/ into the existing root folder docs/. Do not replace the entire root docs folder.

Merge Source Code: Move the contents of humanoid-robotics/src/ into the existing root folder src/.

Replace/Standardize Config and Metadata Files:

Move humanoid-robotics/package.json and humanoid-robotics/package-lock.json to the root folder. Since the root already has these files, replace the root's files with the versions from humanoid-robotics (which likely have more accurate dependencies for the book).

Move the configuration files to the root, adhering to the TypeScript standard:

If humanoid-robotics has a JavaScript file (e.g., docusaurus.config.js), discard it. Keep the root's existing docusaurus.config.ts.

If humanoid-robotics has a JavaScript file (e.g., sidebars.js), discard it. Keep the root's existing sidebars.ts.

Move Remaining Items: Move all other files and folders (e.g., blog, static, etc.) from humanoid-robotics directly into the root folder.

Clean Up: Once all contents have been moved, delete the now-empty humanoid-robotics folder."

## Response Text

Successfully implemented the task to move the Docusaurus project structure from the humanoid-robotics subfolder to the root folder. Here's what was completed:

1. Merged documentation content: Moved all contents from humanoid-robotics/docs/ into the root docs/ folder, preserving existing root docs content.

2. Merged source code: Moved all contents from humanoid-robotics/src/ into the root src/ folder, merging with existing source files.

3. Replaced package files: Replaced the root package.json and package-lock.json with versions from humanoid-robotics to ensure accurate dependencies for the book.

4. Kept existing TypeScript config files: Preserved the existing docusaurus.config.ts and sidebars.ts in the root, discarding the JavaScript versions (docusaurus.config.js and sidebars.js) from humanoid-robotics.

5. Handled remaining items: Confirmed there were no other meaningful files to move (excluding .git and node_modules which should not be moved).

6. Deleted empty folder: Successfully deleted the now-empty humanoid-robotics folder.

The project structure has been successfully consolidated at the root level while maintaining TypeScript standards.

## Outcome

The Docusaurus project structure has been successfully migrated from the humanoid-robotics subfolder to the root directory. All documentation, source code, and configuration files have been properly merged, with dependencies updated to the versions from the humanoid-robotics subproject. The project now follows TypeScript standards with docusaurus.config.ts and sidebars.ts in place.