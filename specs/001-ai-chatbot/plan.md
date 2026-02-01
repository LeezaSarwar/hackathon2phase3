# Implementation Plan: AI-Powered Todo Chatbot

**Branch**:  | **Date**: 2026-01-01 | **Spec**: spec.md

**Input**: Feature specification from specs/001-ai-chatbot/spec.md

## Summary

This plan describes the implementation of Phase III for the Todo Application: an AI-powered chatbot interface for natural language task management. The system integrates OpenAI ChatKit for the frontend, OpenAI Agents SDK for backend orchestration, and MCP (Model Context Protocol) for tool-based task operations. The architecture is stateless, storing all conversation data in PostgreSQL, and maintains backward compatibility with the Phase II web UI.

## Technical Context

**Language/Version**: Python 3.13 (backend), TypeScript/Next.js 15 (frontend)

**Primary Dependencies**: 
- Backend: FastAPI, OpenAI Agents SDK, Official Python MCP SDK, SQLModel
- Frontend: Next.js 15, OpenAI ChatKit, Better Auth

**Storage**: Neon Serverless PostgreSQL (existing from Phase II, extended with conversations and messages tables)

**Testing**: pytest (backend), Jest/Playwright (frontend)

**Target Platform**: Web application (responsive for mobile and desktop)

**Project Type**: Web application with separate frontend and backend

**Performance Goals**:
- Chat endpoint response: < 3 seconds (including AI inference)
- Database query for conversation history: < 300ms
- MCP tool execution: < 200ms each
- Support 10+ concurrent conversations without degradation

**Constraints**:
- Stateless backend architecture (no in-memory conversation storage)
- All task operations via MCP tools for AI (REST API still available for web UI)
- JWT authentication required for all endpoints
- OpenAI API key never exposed to frontend
- Max 50 messages in conversation context

**Scale/Scope**: 
- Single-user scope (no multi-user features)
- 2 new database tables (conversations, messages)
- 5 MCP tools (add_task, list_tasks, complete_task, update_task, delete_task)
- 4 new API endpoints (chat, list conversations, get conversation, delete conversation)

## Constitution Check

All architecture decisions align with the Phase III constitution:

- [x] Separation of Concerns: Frontend (ChatKit), Backend (FastAPI + Agents), MCP Tools, Database
- [x] API-First Design: REST endpoints (Phase II) + MCP tools (Phase III)
- [x] Stateless Backend: All conversation data in database, context rebuilt per request
- [x] MCP-First Design: All AI task operations via MCP tools, no direct DB access
- [x] Security-First: JWT authentication, input validation, API key protection
- [x] Performance Standards: < 3s chat response, < 300ms DB queries
- [x] Required Technologies: OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK, SQLModel
- [x] No Forbidden Technologies: No custom chat UI, no LangChain, no in-memory state

## Project Structure

### Documentation (this feature)

specs/001-ai-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Technology research and architecture decisions
├── data-model.md        # Phase 1: Database schema and data model
├── quickstart.md        # Phase 1: Quick start guide
├── contracts/           # Phase 1: API and MCP tool contracts
│   ├── rest-api.md      # REST API endpoint specifications
│   └── mcp-tools.md     # MCP tool schemas and response formats
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)

### Source Code (repository root)

backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py      # Existing from Phase II
│   │   ├── task.py      # Existing from Phase II
│   │   ├── conversation.py  # NEW: Conversation model
│   │   └── message.py   # NEW: Message model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py      # Existing from Phase II
│   │   ├── task_service.py  # Existing from Phase II
│   │   ├── agent.py     # NEW: OpenAI Agents SDK integration
│   │   └── conversation_service.py  # NEW: Conversation management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py      # Existing from Phase II
│   │   ├── tasks.py     # Existing from Phase II
│   │   └── chat.py      # NEW: Chat endpoint and conversation API
│   └── mcp/
│       ├── __init__.py
│       ├── server.py    # NEW: MCP server initialization
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── add_task.py
│       │   ├── list_tasks.py
│       │   ├── complete_task.py
│       │   ├── update_task.py
│       │   └── delete_task.py
│       └── schemas.py   # MCP tool parameter schemas
└── tests/
    ├── unit/
    │   ├── test_tools/
    │   └── test_agent.py
    ├── integration/
    │   ├── test_chat_endpoint.py
    │   └── test_mcp_tools.py
    └── e2e/
        └── test_conversation_flow.py

frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   ├── chat/
│   │   │   └── page.tsx  # NEW: Chat page with ChatKit
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ChatKitProvider.tsx  # NEW: ChatKit integration
│   │   └── ConversationList.tsx # NEW: Sidebar component
│   ├── lib/
│   │   └── api.ts       # Existing API client, extended for chat
│   └── hooks/
│       └── useAuth.ts   # Existing auth hook
└── tests/

**Structure Decision**: Web application structure with separate frontend and backend, following Phase II pattern. MCP server and chat API added to backend as new modules.

## Complexity Tracking

No constitution violations - all complexity is justified by requirements and aligns with Phase III principles.

## High-Level Architecture

### System Components

Frontend: Next.js + ChatKit
Backend: FastAPI + OpenAI Agents SDK + MCP Server
Database: Neon PostgreSQL (existing with new tables)

### Request Flow: Add Task

1. User types message in ChatKit
2. Frontend sends POST /api/{user_id}/chat
3. Backend validates JWT
4. Backend creates/loads conversation
5. Backend stores user message in database
6. Backend loads conversation history (last 50 messages)
7. Backend builds context array
8. Backend calls OpenAI Agents SDK
9. Agent selects add_task tool
10. MCP server executes tool
11. Tool creates task in database
12. Agent generates conversational response
13. Backend stores assistant response
14. Backend returns response to ChatKit
15. Server forgets everything (stateless)

## Database Schema Extensions

### New Tables

conversations:
- id (serial, primary key)
- user_id (text, foreign key to users)
- created_at (timestamp)
- updated_at (timestamp)

messages:
- id (serial, primary key)
- user_id (text, foreign key to users)
- conversation_id (integer, foreign key to conversations)
- role (text, enum: user or assistant)
- content (text)
- tool_calls (jsonb, optional)
- created_at (timestamp)

Indexes on user_id, conversation_id, created_at, updated_at.

## MCP Tools Design

Five tools: add_task, list_tasks, complete_task, update_task, delete_task

All tools return: success (bool), data (dict), message (str), error (str)

## Chat Endpoint Implementation

POST /api/{user_id}/chat
- Request: message (str), conversation_id (optional int)
- Response: response (str), conversation_id (int), tool_calls (list)
- JWT validation required
- Stateless: Load context from database each request

## ChatKit Integration

Frontend: app/chat/page.tsx with OpenAI ChatKit components
Configuration: NEXT_PUBLIC_OPENAI_DOMAIN_KEY
Domain allowlist configured on OpenAI dashboard

## Error Handling

All errors return friendly messages (no technical jargon)

Error types: 401 (auth), 403 (forbidden), 404 (not found), 500 (internal)

Retry logic for API calls with exponential backoff.

## Testing Strategy

Unit tests for MCP tools
Integration tests for chat endpoint
End-to-end tests for conversation flows

## Deployment

Environment variables for OpenAI API key and ChatKit domain key
Domain allowlist on OpenAI dashboard
HTTPS required in production

## Migration from Phase II

Stays: Auth, users table, tasks table, REST API
New: chat page, chat endpoint, MCP server, conversations table, messages table

Rollback: Disable chat endpoint, keep new tables

## Success Metrics

Chat response time < 3s
DB query time < 300ms
Tool execution < 200ms
Error rate < 1%
Tool accuracy > 95%
