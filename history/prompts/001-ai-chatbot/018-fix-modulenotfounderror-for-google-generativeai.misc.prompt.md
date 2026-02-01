---
id: 18
title: Fix ModuleNotFoundError for google-generativeai
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-chatbot
branch: 001-ai-chatbot
user: user
command: fix missing dependency
labels: ["backend", "error-fix", "pip", "venv"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/.venv (updated packages)
tests:
  - none
---

## Prompt

i add gemini api in  .env and chenge the agent_model=gemini-2.0-flash and i run backend but he given error check this error and solved it [ModuleNotFoundError: No module named 'google']

## Response snapshot

Identified that `google-generativeai` was missing from the virtual environment. Installed `pip` into the venv (as it was missing) and then successfully installed the `google-generativeai` package.

## Outcome

- ✅ Impact: Backend can now properly import the Gemini SDK.
- 🧪 Tests: Package installation confirmed via pip output.
- 📁 Files: Updated backend virtual environment.
- 🔁 Next prompts: None.
- 🧠 Reflection: Ensure that after adding dependencies to `pyproject.toml`, they are also installed in the active environment.
