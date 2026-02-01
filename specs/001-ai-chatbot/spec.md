# Specification: AI-Powered Todo Chatbot

**Branch**: `001-ai-chatbot` | **Date**: 2026-01-01 | **Phase**: III

## Overview

Transform the Phase II web application into an AI-powered chatbot that allows users to manage their todo tasks through natural language conversation. This phase adds OpenAI ChatKit frontend, OpenAI Agents SDK backend, and MCP (Model Context Protocol) server for tool-based task operations.

## Success Criteria

### SC-001: User Adoption
Users can create a task via natural language in under 15 seconds from page load.

### SC-002: Task Management
Users can add, list, complete, update, and delete tasks through chat with > 95% success rate.

### SC-003: Conversation Experience
Average time from user message to assistant response < 5 seconds (including AI inference).

### SC-004: Natural Language Understanding
Agent correctly interprets user intent in > 90% of messages (measured by test suite).

### SC-005: Error Handling
Error messages are user-friendly (not technical jargon) in 100% of error scenarios.

### SC-006: Context Persistence
Conversation context is maintained across 100% of requests (no context loss).

### SC-007: Scalability
System supports 10+ concurrent conversations without performance degradation (> 5s response time).

### SC-008: Security
Zero instances of unauthorized data access (users never see others' conversations or tasks).

### SC-009: Database Performance
Database query for conversation history completes in < 300ms in 95th percentile.

### SC-010: API Reliability
Chat endpoint returns successful response (200 OK) > 99% of time (excluding planned downtime).

### SC-011: Mobile Responsiveness
Chat interface is fully functional on mobile devices (touch interactions, responsive layout).

### SC-012: Backward Compatibility
Phase II web UI continues to function normally (no regression in existing features).

## User Scenarios

### Priority 1 (P1) - Core

#### US-001: First Conversation with AI Assistant

**As a user**, I want to have a conversational interface for managing tasks so that I can interact with the system naturally.

**Acceptance Criteria**:
- [ ] When I navigate to the chat page, I see a welcome message from the AI assistant
- [ ] The welcome message explains what the assistant can do (add, list, complete, update, delete tasks)
- [ ] I can type my first message in a text input field
- [ ] When I send a message, I see it displayed in the conversation
- [ ] The AI responds within 5 seconds
- [ ] My conversation is automatically saved
- [ ] I can see my conversation listed in the sidebar (if implemented)

**User Flow**:
1. User logs in via Better Auth
2. User navigates to chat page
3. ChatKit displays welcome message
4. User types natural language command
5. Assistant responds with action confirmation
6. Conversation persists to database

**Acceptance Scenarios**:
1. AC1.1: User visits chat page for the first time - Expected: Welcome message displayed
2. AC1.2: User sends first message - Expected: Message appears, assistant responds within 5s
3. AC1.3: User refreshes page - Expected: Conversation history persists

#### US-002: Multi-Turn Task Management

**As a user**, I want to manage my tasks through an ongoing conversation.

**Acceptance Criteria**:
- [ ] I can add a task using natural language
- [ ] I can list all my pending tasks
- [ ] I can complete a task by referencing it
- [ ] I can update a task description
- [ ] I can delete a task
- [ ] The assistant maintains context across multiple messages
- [ ] The assistant provides helpful feedback after each action

**User Flow**:
1. User sends: Add a task to buy groceries
2. Assistant responds with confirmation
3. User sends: What tasks do I have?
4. Assistant responds with task list
5. User sends: Complete the grocery shopping task
6. Assistant confirms completion

**Acceptance Scenarios**:
1. AC2.1: User adds task - Expected: Task created with confirmation
2. AC2.2: User lists tasks - Expected: All pending tasks displayed
3. AC2.3: User completes task - Expected: Task marked complete
4. AC2.4: User updates task - Expected: Task updated
5. AC2.5: User deletes task - Expected: Task removed

### Priority 2 (P2) - Enhancement

#### US-003: Error Handling and Recovery

**As a user**, I want clear error messages when something goes wrong.

**Acceptance Criteria**:
- [ ] If a task is not found, I see friendly error message
- [ ] If input is unclear, the assistant asks clarifying questions
- [ ] If the AI service is unavailable, I see a friendly error message
- [ ] Error messages are not technical jargon
- [ ] I can retry failed actions
- [ ] Conversations do not break on errors

#### US-004: Conversation History and Resumption

**As a user**, I want to see and resume my previous conversations.

**Acceptance Criteria**:
- [ ] I can see a list of previous conversations
- [ ] Each conversation shows the first message or a timestamp
- [ ] I can click on a conversation to resume it
- [ ] The full conversation history loads when resumed
- [ ] I can delete conversations I no longer need
- [ ] The assistant maintains context when resuming

#### US-005: Natural Language Understanding

**As a user**, I want the assistant to understand various ways of expressing commands.

**Acceptance Criteria**:
- [ ] Assistant understands add, create, new task as same intent
- [ ] Assistant understands complete, done, finish as same intent
- [ ] Assistant understands delete, remove, get rid of as same intent
- [ ] Assistant handles typos and minor phrasing differences
- [ ] Assistant extracts task descriptions from various sentence structures

## Out of Scope

The following features are explicitly out of scope for Phase III:

- [ ] Voice input/output (text-only conversation)
- [ ] Multi-language support (English only)
- [ ] Task priorities, due dates, or categorization
- [ ] Task sharing between users
- [ ] Multi-user conversations
- [ ] Conversation search or tagging
- [ ] Task reminders or notifications
- [ ] Export/import tasks or conversations
- [ ] Task templates or recurring tasks
- [ ] Conversation summarization or analysis
- [ ] Sentiment analysis or mood tracking
- [ ] Custom AI personality or system prompt customization
- [ ] Integration with external services (calendar, email, etc.)
- [ ] File attachments or image processing
- [ ] Rich text formatting in messages
- [ ] Message editing or deletion by users
- [ ] Conversation branching or forking
- [ ] Analytics dashboard for conversation insights

## Dependencies

### External Services
- OpenAI API: Required for AI inference (gpt-4o-mini or gpt-4o)
- Neon PostgreSQL: Database hosting (existing from Phase II)

### Third-Party Libraries
- OpenAI ChatKit: Frontend chat UI framework
- OpenAI Agents SDK: Backend agent orchestration
- Official Python MCP SDK: MCP server implementation
- Better Auth: Authentication (existing from Phase II)

### Internal Systems
- Phase II Backend: REST API endpoints (still functional)
- Phase II Database Schema: users and tasks tables
- Phase II Authentication: JWT token generation and validation

### Data Sources
- Phase II Database: Neon PostgreSQL with users and tasks tables
- New Tables: conversations and messages (to be added in Phase III)

## Entities

### Conversation
Represents a chat session between a user and the AI assistant.

Properties:
- id: Primary key (integer, auto-increment)
- user_id: Foreign key to users table (string)
- created_at: Creation timestamp (timestamp, auto-set)
- updated_at: Last update timestamp (timestamp, auto-update)

Relationships:
- Many-to-one with User (user_id)
- One-to-many with Messages (conversation_id)

### Message
Represents a single message in a conversation.

Properties:
- id: Primary key (integer, auto-increment)
- user_id: Foreign key to users table (string)
- conversation_id: Foreign key to conversations table (integer)
- role: Message role (enum: user or assistant)
- content: Message text (string)
- tool_calls: JSONB field for tool invocations (JSONB, optional)
- created_at: Creation timestamp (timestamp, auto-set)

Relationships:
- Many-to-one with User (user_id)
- Many-to-one with Conversation (conversation_id)

### Task (from Phase II)
Represents a todo item (existing entity, not new).

Properties:
- id: Primary key (integer, auto-increment)
- user_id: Foreign key to users table (string)
- title: Task description (string)
- completed: Completion status (boolean, default false)
- created_at: Creation timestamp (timestamp, auto-set)
- updated_at: Last update timestamp (timestamp, auto-update)

Relationships:
- Many-to-one with User (user_id)

### User (from Phase II)
Represents a user account (existing entity, not new).

Properties:
- id: Primary key (string, UUID)
- email: User email (string, unique)
- password_hash: Bcrypt hashed password (string)
- created_at: Creation timestamp (timestamp, auto-set)
- updated_at: Last update timestamp (timestamp, auto-update)

Relationships:
- One-to-many with Tasks
- One-to-many with Conversations
- One-to-many with Messages
