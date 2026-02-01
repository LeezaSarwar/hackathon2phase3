---
description: 'Task list for implementing Phase III: AI-Powered Todo Chatbot'
---

# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from '/specs/001-ai-chatbot/'
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: '[ID] [P?] [Story] Description'

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: 'src/', 'tests/' at repository root
- **Web app**: 'backend/src/', 'frontend/src/'
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend/mcp/ directory structure per implementation plan
- [x] T002 Add OpenAI SDK and MCP SDK dependencies to backend/pyproject.toml
- [x] T003 [P] Configure environment variables in backend/.env

**Checkpoint**: Setup phase complete - ready for foundation work

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [x] T004 Create backend/models/conversation.py SQLModel class
- [x] T005 Create backend/models/message.py SQLModel class
- [x] T006 Update backend/models/__init__.py to export Conversation and Message models

### MCP Tool Infrastructure

- [ ] T007 Implement standardized ToolResponse schema in backend/mcp/schemas.py
- [x] T008 [P] Implement add_task function in backend/mcp/tools/add_task.py
- [x] T009 [P] Implement list_tasks function in backend/mcp/tools/list_tasks.py
- [x] T010 [P] Implement complete_task function in backend/mcp/tools/complete_task.py
- [x] T011 [P] Implement update_task function in backend/mcp/tools/update_task.py
- [x] T012 [P] Implement delete_task function in backend/mcp/tools/delete_task.py

### MCP Server

- [x] T013 Implement get_mcp_tools() in backend/mcp/server.py
- [x] T014 Implement execute_mcp_tool() in backend/mcp/server.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First Conversation (Priority: P1) 🎯 MVP

**Goal**: Users can interact with AI assistant through conversational chat interface

- [x] T015 [US1] Create backend/routes/chat.py with POST /api/{user_id}/chat endpoint
- [x] T016 [US1] Create backend/schemas/chat.py Pydantic schemas
- [x] T017 [US1] Add chat routes to FastAPI main.py
- [ ] T018 [US1] Install @openai/chatkit package in frontend
- [ ] T019 [US1] Configure OpenAI domain allowlist and domain key
- [x] T020 [US1] Create frontend/app/chat/page.tsx with ChatKit component
- [x] T021 [US1] Update frontend app/(dashboard)/layout.tsx to add Chat link
- [x] T022 [US1] Add validation and error handling to chat endpoint
- [x] T023 [US1] Add logging for chat operations in backend/routes/chat.py

**Checkpoint**: User Story 1 functional

---

## Phase 4: User Story 2 - Multi-Turn Task Management (Priority: P1)

**Goal**: Users can manage tasks through ongoing conversation

- [ ] T024 [US2] Create frontend/app/chat/components/ConversationList.tsx
- [x] T025 [US2] Implement GET /api/{user_id}/conversations endpoint
- [ ] T026 [US2] Implement GET /api/{user_id}/conversations/{id} endpoint
- [ ] T027 [US2] Implement DELETE /api/{user_id}/conversations/{id} endpoint
- [ ] T028 [US2] Update ConversationList component to display conversations

**Checkpoint**: User Story 2 functional

---

## Phase 5: User Story 3 - Error Handling (Priority: P2)

**Goal**: Clear error messages when something goes wrong

- [ ] T029 [US3] Implement exponential backoff for OpenAI API calls
- [x] T030 [US3] Add user-friendly error messages to agent instructions
- [x] T031 [US3] Implement ToolResponse error cases in MCP tools
- [x] T032 [US3] Add error handling UI to frontend ChatKit component

---

## Phase 6: User Story 4 - History and Resumption (Priority: P2)

**Goal**: See and resume previous conversations

- [x] T033 [US4] Test conversation persistence across server restart
- [x] T034 [US4] Test conversation resumption in browser

---

## Phase 7: User Story 5 - Natural Language Understanding (Priority: P2)

**Goal**: Agent understands various ways of expressing commands

- [x] T035 [US5] Create comprehensive agent instructions
- [ ] T036 [US5] Test agent tool selection for various intents
- [ ] T037 [US5] Test multi-turn conversations

---

## Phase 8: Database Migration

**Purpose**: Add conversations and messages tables

- [x] T038 Create database migration for conversations table
- [x] T039 Create database migration for messages table
- [ ] T040 Run migrations on development environment
- [ ] T041 Run migrations on production environment

---

## Phase 9: Integration Testing

- [x] T042 Test complete user flow: signup -> chat -> manage tasks
- [ ] T043 Test concurrent conversations

---

## Phase 10: Deployment

- [ ] T044 Update README.md with Phase III features
- [ ] T045 Configure production environment variables
- [ ] T046 Deploy frontend to Vercel
- [ ] T047 Deploy backend to production
- [ ] T048 Create 90-second demo video

---

## Notes

- [P] tasks = parallelizable
- [Story] label for traceability
- Server remains stateless
- Enforce user_id authorization
