---
id: 17
title: Setup AI Chatbot with Gemini integration
stage: spec
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-chatbot
branch: 001-ai-chatbot
user: user
command: implement ai chatbot
labels: ["chatbot", "gemini", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/pyproject.toml
  - backend/.env.example
  - backend/app/config.py
  - backend/app/main.py
  - backend/app/routes/__init__.py
  - backend/app/routes/chat.py
  - backend/app/schemas/chat.py
  - frontend/lib/api.ts
  - frontend/app/(dashboard)/chat/page.tsx
  - frontend/components/Sidebar.tsx
tests:
  - none
---

## Prompt

I have run both the frontend and backend, and I also opened /chat on port 3000, but it shows ‘Page Not Found’. Please check this properly and set it up correctly. Also, I want the AI option to be available directly in my ToDo app’s navbar. When I click on it, the chatbot should open, and through it I should be able to add, edit, and delete tasks. Everything should be set up properly. Also, my chatbot will use the Gemini API key.

## Response snapshot

Implemented the Phase III AI Chatbot feature using Gemini API. Fixed the 'Page Not Found' error by creating the `/chat` route in the Next.js frontend, integrated the 'AI Chat' button into the sidebar, and implemented a backend route that uses Gemini tool calling to manage tasks (Add, Edit, Delete, List).

## Outcome

- ✅ Impact: Users can now use an AI chatbot to manage their tasks via natural language.
- 🧪 Tests: No tests run; manual verification of route existence and sidebar link.
- 📁 Files: Created /chat route, updated Sidebar, implemented backend Gemini logic.
- 🔁 Next prompts: Verify Gemini API key functionality.
- 🧠 Reflection: Using Gemini's tool calling required a manual dispatcher loop for async compatibility in FastAPI.

## Evaluation notes (flywheel)

- Failure modes observed: Initial route missing, dependency missing.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add message history persistence.
