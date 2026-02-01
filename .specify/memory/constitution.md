<!--
Sync Impact Report
==================
Version change: 2.0.0 → 3.0.0 (MAJOR - Phase III: AI Chatbot with MCP)

Modified principles:
- No Phase II principles removed - all are carried forward
- Phase II principles extended with AI/MCP specific constraints

Added sections:
- MCP-First Design Principle (new architectural principle)
- MCP Tool Design Principles
- Conversation Flow Principles
- Database Schema Extensions (conversations, messages tables)
- Frontend (ChatKit) Principles
- Agent Behavior Constraints
- Testing Requirements (MCP tools, Agent integration)
- Development Workflow Standards (MCP server structure)
- Migration from Phase II (what changes vs. what stays the same)
- API Endpoints Summary (Phase II + Phase III)
- Environment Variables (Extended for AI)
- Non-Negotiables (8 AI-specific constraints)
- Quality Metrics (AI-specific success metrics)
- Phase III-Specific Risks

Updated technology stack:
- Added: OpenAI Agents SDK, Official MCP SDK, OpenAI ChatKit
- Extended: FastAPI backend now includes chat endpoint and MCP server
- Constraint: All task operations via MCP tools for AI (REST still available for web UI)

Removed sections:
- None

Templates requiring updates:
- .specify/templates/plan-template.md: ✅ Compatible (constitution check gates unchanged)
- .specify/templates/spec-template.md: ✅ Compatible (user stories still required)
- .specify/templates/tasks-template.md: ✅ Compatible (task categorization unchanged)

Follow-up TODOs: None
-->

# Todo Application Constitution - Phase III

## Purpose

This constitution defines the non-negotiable principles, architectural constraints, and quality standards for the Todo Application across all phases. Phase III extends Phase II by adding conversational AI capabilities through MCP (Model Context Protocol) tools and OpenAI Agents SDK.

## Core Principles

### I. Separation of Concerns

The application MUST maintain strict boundaries between frontend, backend, data, and AI layers.

- **Frontend (Next.js + ChatKit)**: Handles UI/UX, client-side state, and user interactions ONLY
- **Backend (FastAPI)**: Manages business logic, data validation, database operations, and chat orchestration
- **MCP Server**: Exposes task operations as tools for AI agent consumption
- **OpenAI Agents SDK**: Natural language understanding and tool selection
- **Database (Neon PostgreSQL)**: Serves as the single source of truth for all persistent data (tasks, conversations, messages)
- No business logic in the frontend beyond UI state management
- No UI rendering logic in the backend
- No direct database calls from AI agent (MUST use MCP tools)

**Rationale**: Clear separation enables independent scaling, testing, and deployment of each layer while adding AI capabilities without disrupting existing architecture.

### II. API-First Design

All data access MUST flow through well-defined API contracts.

- RESTful API design with clear, predictable endpoints (Phase II - Web UI)
- MCP tool definitions for AI agent consumption (Phase III - Chatbot)
- All data access MUST flow through documented endpoints or MCP tools
- Frontend MUST NEVER directly access the database
- Agent MUST NEVER directly access the database (use MCP tools)
- API responses and tool returns MUST be consistent and well-typed
- Contracts MUST be defined before implementation

**Rationale**: API-first ensures frontend, backend, and AI agent can evolve independently with clear integration points.

### III. Stateless Backend

Backend services MUST be stateless to enable horizontal scaling.

- Session data MUST be stored in database, not in memory
- Conversation history MUST be stored in database, not in memory
- Horizontal scalability MUST be possible without code changes
- JWT tokens for authentication (no server-side sessions)
- No request-scoped global state
- Each request MUST be self-contained
- Server rebuilds conversation context fresh every request

**Rationale**: Stateless architecture enables load balancing, zero-downtime deployments, and reliable conversation management across server restarts.

### IV. MCP-First Design (Phase III)

All task operations for AI MUST be exposed as MCP tools.

- AI agent routes natural language to appropriate MCP tools
- MCP tools are the single interface between AI and database
- Tools must be idempotent and well-documented
- No business logic in the chat endpoint - delegate to tools
- Tool descriptions must be clear for AI understanding
- Each tool must validate inputs before execution
- Tools must return consistent response format
- Error messages must be AI-friendly (not technical jargon)

**Rationale**: MCP tools provide a structured, secure, and maintainable interface for AI agents to interact with application data.

### V. Security-First

Security MUST be built into every layer, not added as an afterthought.

- All API endpoints and MCP tools MUST require valid JWT
- Backend MUST validate ALL inputs (never trust the frontend or agent)
- SQL injection prevention through ORM (no raw SQL)
- XSS prevention through React's built-in escaping
- CORS properly configured (whitelist frontend URL only)
- No user can access another user's data, tasks, or conversations
- OpenAI API key never exposed to frontend
- API calls to OpenAI only from backend

**Rationale**: A todo app with conversations contains personal data; security breaches destroy user trust permanently.

### VI. Performance Standards

The application MUST meet defined performance budgets.

- **Frontend**: First Contentful Paint (FCP) < 1.5 seconds
- **Frontend**: Time to Interactive (TTI) < 3 seconds
- **Backend (REST API)**: API response time < 200ms for CRUD operations
- **Backend (Chat)**: Chat endpoint response < 3 seconds (including AI inference)
- **MCP Tools**: Tool execution < 200ms each
- **Database**: Queries MUST use indexes on user_id and conversation_id
- **Conversation History**: Database query < 300ms
- **Total Chat Wait Time**: < 5 seconds from user message to response
- No N+1 queries (use joins or batching)

**Rationale**: Performance directly impacts user experience and retention. AI chatbots demand fast responses to feel conversational.

## Technology Stack Constraints

### Required Technologies

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| Frontend | Next.js | 15+ (App Router ONLY, no Pages Router) |
| Frontend Chat UI | OpenAI ChatKit | Official UI framework |
| Backend | Python + FastAPI | Python 3.13+ |
| AI Framework | OpenAI Agents SDK | Official SDK |
| MCP | Official Python MCP SDK | Official SDK |
| ORM | SQLModel | NOT SQLAlchemy directly |
| Database | Neon Serverless PostgreSQL | - |
| Authentication | Better Auth | With JWT plugin |
| AI Model | gpt-4o-mini or gpt-4o | Configurable via AGENT_MODEL |
| Python Package Manager | UV | - |
| JS Package Manager | npm or pnpm | - |

### Forbidden Technologies

The following are explicitly FORBIDDEN in this project:

- ❌ Custom chat UI implementations (MUST use OpenAI ChatKit)
- ❌ Storing conversation state in Redis/memory (MUST use database)
- ❌ Direct database calls from AI agent (MUST use MCP tools)
- ❌ Synchronous blocking operations in chat endpoint
- ❌ Custom MCP server implementations (MUST use official SDK)
- ❌ LangChain or other agent frameworks (MUST use OpenAI Agents SDK)
- ❌ Class-based React components
- ❌ localStorage/sessionStorage for authentication tokens
- ❌ Inline SQL queries (MUST use SQLModel)
- ❌ Global state management libraries (Zustand, Redux) - use React Context if needed
- ❌ Custom authentication implementations (MUST use Better Auth)
- ❌ Pages Router in Next.js
- ❌ CSS Modules or inline styles (use Tailwind CSS)
- ❌ `.then()` chains (use async/await)

## Code Quality Standards

### TypeScript/JavaScript Standards

- All frontend code MUST use TypeScript with strict mode enabled
- No `any` types except in unavoidable third-party integrations
- React Server Components by default; Client Components ONLY when needed
- Async/await for all asynchronous operations
- Tailwind CSS for all styling

### Python Standards

- Type hints REQUIRED for all function signatures
- Pydantic models for all request/response schemas
- Async/await for all I/O operations (database, external APIs, AI calls)
- No raw SQL - MUST use SQLModel query builder
- FastAPI dependency injection for database sessions
- MCP tools MUST have explicit JSON schema for parameters

### Error Handling

All API endpoints MUST return consistent error shapes:

```json
{
  "error": "string",
  "detail": "string",
  "code": "ERROR_CODE"
}
```

All MCP tools MUST return consistent response format:

```json
{
    "success": bool,
    "data": {...},
    "message": "string"
}
```

All MCP tool errors MUST return:

```json
{
    "success": false,
    "error": "ERROR_CODE",
    "message": "string"
}
```

- Frontend MUST handle all error states with user-friendly messages
- Agent MUST translate technical errors to friendly language
- No silent failures - log all errors appropriately
- Errors MUST NOT expose internal implementation details

## Security Principles

### Authentication & Authorization

- All API endpoints and chat endpoints MUST require valid JWT
- JWT tokens MUST expire after 7 days
- Tokens MUST be stored in httpOnly cookies (NOT localStorage)
- User ID from token MUST match user_id in URL path
- MCP tools MUST receive and validate user_id parameter
- No user can access another user's data, tasks, or conversations

### Input Validation

- Backend MUST validate ALL inputs (never trust the frontend or agent)
- SQL injection prevention through ORM (no raw SQL)
- XSS prevention through React's built-in escaping
- CORS MUST be configured to whitelist frontend URL only
- User messages sanitized before processing (prompt injection prevention)

### Data Privacy

- Passwords hashed with bcrypt (handled by Better Auth)
- Environment variables for ALL secrets (no hardcoded credentials)
- Database connection strings MUST NEVER be exposed to frontend
- OpenAI API key never exposed to frontend or logs
- No API keys in error messages

## MCP Tool Design Principles

### Tool Naming Convention

MCP tools MUST follow verb_noun pattern:

```
add_task       (verb_noun pattern)
list_tasks     (verb_noun pattern)
complete_task  (verb_noun pattern)
update_task    (verb_noun pattern)
delete_task    (verb_noun pattern)
```

### Tool Parameter Standards

- `user_id` required in all tools (for authorization)
- Use descriptive parameter names
- Make parameters optional when appropriate
- Provide default values where sensible
- Use Pydantic models for complex parameters
- All tools must have explicit JSON schema for parameters

### Tool Response Format

All MCP tools MUST return:

```python
{
    "success": bool,
    "data": {...},  # Tool-specific data
    "message": str  # Human-readable confirmation
}
```

### Tool Error Handling

All MCP tools MUST return:

```python
{
    "success": false,
    "error": "TASK_NOT_FOUND",
    "message": "I couldn't find that task"
}
```

Error codes MUST be:
- Machine-readable for agent routing
- Human-friendly for conversation flow
- Not technical jargon

## Conversation Flow Principles

### Stateless Request Cycle

1. Receive user message
2. Authenticate user (JWT)
3. Load conversation history from DB
4. Append user message to history
5. Store user message in DB
6. Build context array for agent
7. Run agent with MCP tools
8. Collect tool calls and results
9. Generate assistant response
10. Store assistant response in DB
11. Return response to client
12. Server forgets everything (stateless)

### Context Building Strategy

- Include full conversation history (user + assistant messages)
- Include tool calls and results in context
- Limit to last 50 messages (MAX_CONVERSATION_MESSAGES) to avoid token limits
- No message summarization (maintain full fidelity)
- Context rebuilt fresh every request

### Error Recovery

- If agent fails, return friendly error message
- If tool fails, agent should acknowledge and ask for retry
- If database fails, return 500 with retry instruction
- Never expose technical errors to user

## Agent Behavior Constraints

### Tool Selection Logic

- Agent must intelligently select appropriate tools
- When ambiguous, ask clarifying questions before acting
- Chain multiple tools if needed (e.g., list_tasks then delete_task)
- Confirm destructive actions (delete, complete)

### Conversational Guidelines

- Use friendly, natural language
- Avoid robotic responses ("Task has been created" → "Got it! I've added 'Buy groceries' to your list.")
- Provide context in responses ("You now have 5 pending tasks")
- Acknowledge limitations ("I can't do that, but I can...")

### Error Behavior

- Never show stack traces or technical errors
- Translate errors to friendly language
- Suggest corrective actions
- Maintain conversation flow even after errors

## Database Design Standards

All tables MUST have:

- Primary key (auto-incrementing integer or UUID)
- `created_at` timestamp (auto-set on creation)
- `updated_at` timestamp (auto-updated on modification)

Additional requirements:

- Foreign keys MUST be enforced at database level
- Indexes REQUIRED on frequently queried columns
- `user_id` MUST be indexed on all user-owned tables
- `conversation_id` MUST be indexed on messages table
- Messages immutable after creation (no updates/deletes)
- Conversation `updated_at` refreshed on new message

### Phase III Database Extensions

**Conversations Table**:

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
```

**Messages Table**:

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,  -- Store tool invocations
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## Frontend (ChatKit) Principles

### ChatKit Configuration

- Use OpenAI ChatKit official package
- Configure domain allowlist on OpenAI dashboard
- Pass `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` from environment
- Use ChatKit's built-in message display components

### Message Display Standards

- User messages aligned right (blue background)
- Assistant messages aligned left (gray background)
- Show typing indicator while waiting for response
- Display tool calls visually (optional enhancement)
- Show error messages in red with retry option

### Conversation Management

- Start new conversation button
- List previous conversations (sidebar)
- Resume existing conversation by clicking it
- Delete conversation button (with confirmation)

## Testing Requirements

### MCP Tool Testing

- Unit test each tool in isolation
- Test with valid and invalid inputs
- Test authorization (user_id validation)
- Test database failures (simulate and handle)

### Agent Integration Testing

- Test natural language understanding
- Test tool selection accuracy
- Test multi-turn conversations
- Test conversation persistence across requests

### End-to-End Testing

- Test complete user flows (signup → chat → task management)
- Test conversation resumption
- Test error handling
- Test concurrent users

## Development Workflow

### Monorepo Structure

```
hackathon-todo/
├── frontend/          # Next.js + ChatKit application
├── backend/           # FastAPI + MCP server application
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py         # MCP server initialization
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── complete_task.py
│   │   │   ├── update_task.py
│   │   │   └── delete_task.py
│   │   └── schemas.py        # Tool parameter schemas
│   └── src/
├── specs/             # Spec-Kit specifications
├── .specify/          # Specify configuration
├── docker-compose.yml # Local development setup
└── README.md
```

### Environment Management

- `.env.local` for local development (git-ignored)
- `.env.example` MUST be maintained with all required variables (no values)
- Production secrets via deployment platform environment variables

**Backend Environment Variables**:

```bash
# Existing from Phase II
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
CORS_ORIGINS=http://localhost:3000

# New for Phase III
OPENAI_API_KEY=sk-...
AGENT_MODEL=gpt-4o-mini  # or gpt-4o
MAX_CONVERSATION_MESSAGES=50
```

**Frontend Environment Variables**:

```bash
# Existing from Phase II
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=...

# New for Phase III
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...
NEXT_PUBLIC_CHATKIT_ENABLED=true
```

### Change Process

1. **Specification**: Document user story with acceptance criteria before implementation
2. **Design**: For non-trivial changes, create implementation plan in `specs/<feature>/plan.md`
3. **Implementation**: Follow the plan; commit in logical increments
4. **Verification**: Run tests and manual verification against acceptance criteria
5. **Review**: Code review required for shared/production branches

### Branch Strategy

- `main`: Production-ready code only
- Feature branches: `<issue-number>-<brief-description>`
- Keep branches short-lived; merge frequently

### MCP Server Development Pattern

```python
from openai import OpenAI
from mcp import MCPServer

# Initialize MCP server with tools
mcp_server = MCPServer(tools=[
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    update_task_tool,
    delete_task_tool
])

# Run agent with tools
agent = OpenAI.beta.agents.create(
    name="Todo Assistant",
    instructions="You help users manage their tasks...",
    tools=mcp_server.get_tool_definitions()
)

# Execute agent with conversation history
result = agent.run(messages=conversation_history)
```

## API Endpoints Summary

### Phase II - REST API (Still Active)

- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User authentication
- `GET /api/{user_id}/tasks` - List tasks (Web UI)
- `POST /api/{user_id}/tasks` - Create task (Web UI)
- `PUT /api/{user_id}/tasks/{id}` - Update task (Web UI)
- `DELETE /api/{user_id}/tasks/{id}` - Delete task (Web UI)
- `PATCH /api/{user_id}/tasks/{id}/complete` - Complete task (Web UI)

### Phase III - Chat API (New)

- `POST /api/{user_id}/chat` - Main chat endpoint (AI agent)
- `GET /api/{user_id}/conversations` - List conversations
- `GET /api/{user_id}/conversations/{id}` - Get conversation history
- `DELETE /api/{user_id}/conversations/{id}` - Delete conversation

## Migration from Phase II

### What Changes from Phase II

| Aspect | Phase II (Web UI) | Phase III (AI Chatbot) |
|--------|-------------------|------------------------|
| Interface | Visual forms and buttons | Natural language chat |
| Task Operations | Direct REST API calls | Via AI agent + MCP tools |
| User Interaction | Clicks and typing | Conversational commands |
| Frontend | Custom React components | OpenAI ChatKit |
| Backend | REST endpoints | Chat endpoint + MCP server |

### What Stays the Same

- Authentication (Better Auth + JWT)
- Database (Neon PostgreSQL)
- Task data model (users, tasks tables)
- Core CRUD operations (still work via REST if needed)
- All Phase II principles (Separation of Concerns, API-First, Stateless, Security, Performance)

### Backward Compatibility

- **Phase II REST API remains functional** for web UI
- Phase III adds new `/api/{user_id}/chat` endpoint
- Both interfaces share same task database
- Users can switch between web UI and chat UI

## Non-Negotiables

These CANNOT be compromised under any circumstances:

1. ✅ **Stateless architecture** - No conversation state in memory
2. ✅ **MCP tools only** - All task operations via MCP, not direct DB calls
3. ✅ **User isolation** - Users never see others' conversations or tasks
4. ✅ **Conversation persistence** - All messages stored in database
5. ✅ **Authentication required** - No unauthenticated chat access
6. ✅ **Official SDKs only** - OpenAI Agents SDK + Official MCP SDK
7. ✅ **No prompt injection** - User messages sanitized before processing
8. ✅ **Graceful errors** - Never show technical errors to users

## Quality Metrics

### Success Metrics

- Agent selects correct tool > 95% of the time
- Average response time < 3 seconds
- Conversation context maintained across 100% of requests
- Zero conversation data loss incidents
- Tool execution success rate > 99%

### User Experience Metrics

- Natural language understanding feels accurate
- Responses feel conversational (not robotic)
- Errors handled gracefully without confusion
- Users prefer chat over web UI (subjective feedback)

## Phase III-Specific Risks

| Risk | Mitigation |
|------|-----------|
| OpenAI API rate limits | Implement exponential backoff, queue system |
| High API costs | Use gpt-4o-mini, limit conversation context |
| Agent hallucinations | Clear tool schemas, validate outputs |
| Long response times | Stream responses, show typing indicators |
| Conversation context too large | Limit to last 50 messages, token counting |
| MCP tool failures | Retry logic, fallback responses |

## Governance

### Constitutional Authority

This constitution establishes the foundational principles for the Todo Application across all phases. All development decisions, code reviews, and architectural choices MUST align with these principles.

### Amendment Process

1. Propose amendment with rationale in a pull request modifying this file
2. Document impact on existing code and templates
3. Obtain team consensus (or owner approval for solo projects)
4. Update version according to semantic versioning:
   - **MAJOR**: Principle removal, fundamental redefinition, breaking architectural change, or major phase transition (e.g., Phase II → Phase III)
   - **MINOR**: New principle or section added, materially expanded guidance
   - **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

- Code reviews MUST verify alignment with constitutional principles
- Violations require either code change or documented exception with justification
- Repeated violations indicate need for constitution review or training

### Constitution Check Gates

Before implementation, verify:

- [ ] Architecture follows Separation of Concerns (Frontend/Backend/Database/AI)
- [ ] All data access flows through API endpoints or MCP tools
- [ ] Backend is stateless (no in-memory session or conversation data)
- [ ] Security requirements met (JWT, input validation, CORS, API key protection)
- [ ] Performance budgets defined and achievable (< 3s chat response)
- [ ] Required technologies used (no forbidden technologies)
- [ ] Code quality standards met (TypeScript strict, Python type hints, MCP tool schemas)
- [ ] MCP tools follow naming convention and response format standards
- [ ] Agent behavior constraints documented (friendly, confirm actions, handle ambiguity)
- [ ] Conversation flow is stateless with database persistence

**Version**: 3.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2026-01-01
