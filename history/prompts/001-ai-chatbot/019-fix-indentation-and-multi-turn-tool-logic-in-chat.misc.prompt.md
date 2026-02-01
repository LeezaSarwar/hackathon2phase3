---
id: 19
title: Fix indentation and multi-turn tool logic in chat.py
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-chatbot
branch: 001-ai-chatbot
user: user
command: debug chatbot error
labels: ["backend", "gemini", "bug-fix", "tool-use"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/routes/chat.py
tests:
  - none
---

## Prompt

I have added the API, but even then when I ask the AI to add tasks, it says: ‘Sorry, I encountered an error. Please make sure your Gemini API key is configured correctly.’

## Response snapshot

Identified and fixed a critical indentation bug in the `chat_endpoint` where most of the tool-handling logic was skipped unless the response had exactly one part with a function call (and potentially caused NameErrors). Also added a manual client initialization fallback and debug logging to ensure the API key is active.

## Outcome

- ✅ Impact: Corrected the logic for handling function calls from Gemini.
- 🧪 Tests: Debug prints added for manual verification.
- 📁 Files: backend/app/routes/chat.py
- 🔁 Next prompts: None.
- 🧠 Reflection: Indentation mistakes in multi-step SDK logic can easily break the entire tool-calling chain.
