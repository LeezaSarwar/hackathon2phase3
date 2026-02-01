<!-- ---
id: 003
title: Phase III AI Chatbot Constitution
stage: constitution
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "phase-iii", "ai-chatbot", "mcp", "major-update"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
--- -->

## Prompt

/sp.constitution

# CONSTITUTION.md - Phase III: AI-Powered Todo Chatbot

## Purpose
This constitution defines the non-negotiable principles, architectural constraints, and quality standards for the Phase III Todo AI Chatbot. This phase extends Phase II by adding conversational AI capabilities through MCP (Model Context Protocol) tools.

---

## 1. Architectural Principles

### 1.1 Stateless Architecture
- **Backend must be completely stateless** - no conversation state in memory
- All conversation history stored in database
- Each request is self-contained and independent
- Server can restart without losing conversations
- Horizontal scaling must be possible without code changes

### 1.2 MCP-First Design
- **All task operations exposed as MCP tools** (not REST endpoints for chat)
- AI agent routes natural language to appropriate MCP tools
- MCP tools are the single interface between AI and database
- Tools must be idempotent and well-documented
- No business logic in the chat endpoint - delegate to tools

### 1.3 Separation of Concerns
- **Frontend (ChatKit)**: Conversational UI, message display
- **Chat Endpoint**: Orchestrates agent, manages conversation flow
- **OpenAI Agents SDK**: Natural language understanding, tool selection
- **MCP Server**: Tool definitions and implementations
- **Database**: Single source of truth for tasks and conversations

### 1.4 Conversation Context Management
- Full conversation history loaded from database on each request
- Context includes all previous messages (user + assistant)
- Agent sees complete history to maintain coherent conversations
- No memory leaks - context rebuilt fresh every request

---

## 2. Technology Stack Constraints

### 2.1 s
- Rate limiting on chat endpoint (prevent abuse)

### 4.3 API Key Security
- OpenAI API key never exposed to frontend
- API calls to OpenAI only from backend
- No API key in logs or error messages
- Separate keys for development and production

---

## 5. Performance Standards

### 5.1 Response Time Targets
- Chat endpoint response: < 3 seconds (including AI inference)
- MCP tool execution: < 200ms each
- Database query for conversation history: < 300ms
- Total user wait time: < 5 seconds

### 5.2 Scalability Requirements
- Support 100 concurrent users
- Handle conversations with 100+ messages
- No memory leaks from conversation context
- DRequired Technologies
- **Frontend**: OpenAI ChatKit (official UI framework)
- **Backend**: Python 3.13+ with FastAPI (from Phase II)
- **AI Framework**: OpenAI Agents SDK (official)
- **MCP**: Official Python MCP SDK
- **ORM**: SQLModel (continue from Phase II)
- **Database**: Neon Serverless PostgreSQL (same as Phase II)
- **Authentication**: Better Auth with JWT (continue from Phase II)

### 2.2 Forbidden Technologies
- ❌ No custom chat UI implementations (must use ChatKit)
- ❌ No storing conversation state in Redis/memory
- ❌ No direct database calls from agent (must use MCP tools)
- ❌ No synchronous blocking operations in chat endpoint
- ❌ No custom MCP server implementations (use official SDK)
- ❌ No LangChain or other agent frameworks (must use OpenAI Agents SDK)

---

## 3. Code Quality Standards

### 3.1 MCP Tool Standards
- Each tool must have explicit JSON schema for parameters
- Tool descriptions must be clear for AI understanding
- All tools must validate inputs before execution
- Tools must return consistent response format
- No side effects - tools should be pure operations
- Error messages must be AI-friendly (not technical jargon)

### 3.2 Agent Behavior Standards
- Agent must confirm actions before executing destructive operations
- Agent must provide friendly, conversational responses
- Agent must handle ambiguity by asking clarifying questions
- Agent must never hallucinate task IDs or data
- Agent must gracefully handle tool failures

### 3.3 Conversation Standards
- Every message must be stored with timestamp
- User messages stored before processing
- Assistant responses stored after generation
- No message loss even on server crash
- Conversation IDs must be immutable

---

## 4. Security Principles

### 4.1 Authentication & Authorization (Extended from Phase II)
- All chat endpoints require valid JWT
- `user_id` from JWT must match `user_id` in URL path
- MCP tools must receive and validate `user_id` parameter
- No user can access another user's conversations or tasks
- OpenAI atabase connection pooling configured

### 5.3 AI Efficiency
- Use gpt-4o-mini for cost efficiency (or gpt-4o if needed)
- Limit context to last 50 messages (or 4000 tokens)
- Stream responses to frontend (if ChatKit supports)
- Cache conversation history in single query

---

## 6. MCP Tool Design Principles

### 6.1 Tool Naming Convention
```
add_task       (verb_noun pattern)
list_tasks     (verb_noun pattern)
complete_task  (verb_noun pattern)
update_task    (verb_noun pattern)
delete_task    (verb_noun pattern)
```

### 6.2 Tool Parameter Standards
- `user_id` required in all tools (for authorization)
- Use descriptive parameter names
- Make parameters optional when appropriate
- Provide default values where sensible
- Use Pydantic models for complex parameters

### 6.3 Tool Response Format
```python
{
    "success": bool,
    "data": {...},  # Tool-specific data
    "message": str  # Human-readable confirmation
}
```

### 6.4 Tool Error Handling
```python
{
    "success": false,
    "error": "TASK_NOT_FOUND",
    "message": "I couldn't find that task"
}
```

---

## 7. Conversation Flow Principles

### 7.1 Stateless Request Cycle
```
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
```

### 7.2 Context Building Strategy
- Include full conversation history (user + assistant messages)
- Include tool calls and results in context
- Limit to last 50 messages (to avoid token limits)
- No message summarization (maintain full fidelity)

### 7.3 Error Recovery
- If agent fails, return friendly error message
- If tool fails, agent should acknowledge and ask for retry
- If database fails, return 500 with retry instruction
- Never expose technical errors to user

---

## 8. Database Schema Extensions

### 8.1 New Tables (in addition to Phase II)

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

### 8.2 Data Integrity Rules
- Each message must belong to a conversation
- Each conversation must belong to a user
- Messages immutable after creation (no updates/deletes)
- Conversation `updated_at` refreshed on new message

---

## 9. Frontend (ChatKit) Principles

### 9.1 ChatKit Configuration
- Use OpenAI ChatKit official package
- Configure domain allowlist on OpenAI dashboard
- Pass `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` from environment
- Use ChatKit's built-in message display components

### 9.2 Message Display Standards
- User messages aligned right (blue background)
- Assistant messages aligned left (gray background)
- Show typing indicator while waiting for response
- Display tool calls visually (optional enhancement)
- Show error messages in red with retry option

### 9.3 Conversation Management
- Start new conversation button
- List previous conversations (sidebar)
- Resume existing conversation by clicking it
- Delete conversation button (with confirmation)

---

## 10. Agent Behavior Constraints

### 10.1 Tool Selection Logic
- Agent must intelligently select appropriate tools
- When ambiguous, ask clarifying questions before acting
- Chain multiple tools if needed (e.g., list_tasks then delete_task)
- Confirm destructive actions (delete, complete)

### 10.2 Conversational Guidelines
- Use friendly, natural language
- Avoid robotic responses ("Task has been created" → "Got it! I've added 'Buy groceries' to your list.")
- Provide context in responses ("You now have 5 pending tasks")
- Acknowledge limitations ("I can't do that, but I can...")

### 10.3 Error Behavior
- Never show stack traces or technical errors
- Translate errors to friendly language
- Suggest corrective actions
- Maintain conversation flow even after errors

---

## 11. Testing Requirements

### 11.1 MCP Tool Testing
- Unit test each tool in isolation
- Test with valid and invalid inputs
- Test authorization (user_id validation)
- Test database failures (simulate and handle)

### 11.2 Agent Integration Testing
- Test natural language understanding
- Test tool selection accuracy
- Test multi-turn conversations
- Test conversation persistence across requests

### 11.3 End-to-End Testing
- Test complete user flows (signup → chat → task management)
- Test conversation resumption
- Test error handling
- Test concurrent users

---

## 12. Development Workflow Standards

### 12.1 MCP Server Development
```
backend/
├── mcp/
│   ├── __init__.py
│   ├── server.py         # MCP server initialization
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── add_task.py
│   │   ├── list_tasks.py
│   │   ├── complete_task.py
│   │   ├── update_task.py
│   │   └── delete_task.py
│   └── schemas.py        # Tool parameter schemas
```

### 12.2 Agent Integration Pattern
```python
from openai import OpenAI
from mcp import MCPServer

# Initialize MCP server with tools
mcp_server = MCPServer(tools=[
    add_task_tool,
    list_tasks_tool,
    # ...
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

---

## 13. Migration from Phase II

### 13.1 What Changes from Phase II

| Aspect | Phase II (Web UI) | Phase III (AI Chatbot) |
|--------|-------------------|------------------------|
| Interface | Visual forms and buttons | Natural language chat |
| Task Operations | Direct REST API calls | Via AI agent + MCP tools |
| User Interaction | Clicks and typing | Conversational commands |
| Frontend | Custom React components | OpenAI ChatKit |
| Backend | REST endpoints | Chat endpoint + MCP server |

### 13.2 What Stays the Same
- Authentication (Better Auth + JWT)
- Database (Neon PostgreSQL)
- Task data model (users, tasks tables)
- Core CRUD operations (still work via REST if needed)

### 13.3 Backward Compatibility
- **Phase II REST API remains functional** for web UI
- Phase III adds new `/api/{user_id}/chat` endpoint
- Both interfaces share same task database
- Users can switch between web UI and chat UI

---

## 14. API Endpoints Summary

### 14.1 Existing (Phase II - Still Active)
- `POST /api/auth/signup`
- `POST /api/auth/signin`
- `GET /api/{user_id}/tasks`
- `POST /api/{user_id}/tasks`
- `PUT /api/{user_id}/tasks/{id}`
- `DELETE /api/{user_id}/tasks/{id}`
- `PATCH /api/{user_id}/tasks/{id}/complete`

### 14.2 New (Phase III)
- `POST /api/{user_id}/chat` - Main chat endpoint
- `GET /api/{user_id}/conversations` - List conversations
- `GET /api/{user_id}/conversations/{id}` - Get conversation history
- `DELETE /api/{user_id}/conversations/{id}` - Delete conversation

---

## 15. Environment Variables (Extended)

### 15.1 Backend (`.env`)
```
# Existing from Phase II
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
CORS_ORIGINS=http://localhost:3000

# New for Phase III
OPENAI_API_KEY=sk-...
AGENT_MODEL=gpt-4o-mini  # or gpt-4o
MAX_CONVERSATION_MESSAGES=50
```

### 15.2 Frontend (`.env.local`)
```
# Existing from Phase II
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=...

# New for Phase III
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...
NEXT_PUBLIC_CHATKIT_ENABLED=true
```

---

## 16. Non-Negotiables

These CANNOT be compromised under any circumstances:

1. ✅ **Stateless architecture** - No conversation state in memory
2. ✅ **MCP tools only** - All task operations via MCP, not direct DB calls
3. ✅ **User isolation** - Users never see others' conversations or tasks
4. ✅ **Conversation persistence** - All messages stored in database
5. ✅ **Authentication required** - No unauthenticated chat access
6. ✅ **Official SDKs only** - OpenAI Agents SDK + Official MCP SDK
7. ✅ **No prompt injection** - User messages sanitized before processing
8. ✅ **Graceful errors** - Never show technical errors to users

---

## 17. Quality Metrics

### 17.1 Success Metrics
- Agent selects correct tool > 95% of the time
- Average response time < 3 seconds
- Conversation context maintained across 100% of requests
- Zero conversation data loss incidents
- Tool execution success rate > 99%

### 17.2 User Experience Metrics
- Natural language understanding feels accurate
- Responses feel conversational (not robotic)
- Errors handled gracefully without confusion
- Users prefer chat over web UI (subjective feedback)

---

## 18. Change Management

### 18.1 When to Update This Constitution
- Adding new MCP tools
- Changing agent instructions or behavior
- Modifying conversation storage strategy
- Introducing new AI models or frameworks

### 18.2 When NOT to Update This Constitution
- Adding new natural language patterns (update agent instructions)
- Changing UI styling (ChatKit configuration)
- Performance tuning (optimization, not architecture)

---

## 19. Deployment Considerations

### 19.1 OpenAI API Key Management
- Use separate API keys for dev/staging/production
- Monitor API usage and set billing alerts
- Rotate keys quarterly
- Never commit keys to git

### 19.2 ChatKit Domain Allowlist
- Add all deployment domains to OpenAI allowlist
- Get domain key for each environment
- Test thoroughly before production launch

### 19.3 Database Considerations
- Conversations and messages tables can grow large
- Plan for archival strategy (optional)
- Monitor database size and performance
- Consider message retention policy (e.g., 90 days)

---

## 20. Phase III-Specific Risks

| Risk | Mitigation |
|------|-----------|
| OpenAI API rate limits | Implement exponential backoff, queue system |
| High API costs | Use gpt-4o-mini, limit conversation context |
| Agent hallucinations | Clear tool schemas, validate outputs |
| Long response times | Stream responses, show typing indicators |
| Conversation context too large | Limit to last 50 messages, token counting |
| MCP tool failures | Retry logic, fallback responses |

---

## Version History
- **v1.0** (Phase III) - Initial constitution for AI chatbot

---

**Remember**: This constitution extends Phase II. All Phase II principles (security, performance, code quality) still apply. Phase III adds conversational AI on top of the existing foundation.

**Next Steps**:
1. Review `speckit.specify` (Phase III requirements)
2. Study `speckit.plan` (Phase III architecture)
3. Implement `speckit.tasks` (Phase III breakdown)
4. Use Claude Code for spec-driven implementation

## Response snapshot

Updated constitution from v2.0.0 to v3.0.0 (MAJOR version bump - Phase III transition) with:

**Phase II principles preserved and extended:**
1. Separation of Concerns (added AI and MCP layers)
2. API-First Design (now includes MCP tools)
3. Stateless Backend (added conversation state to database requirement)
4. Security-First (extended for AI/OpenAI integration)
5. Performance Standards (added chat-specific budgets)

**New principle added:**
6. MCP-First Design (AI task operations via MCP tools)

**Major new sections added:**
- MCP Tool Design Principles (naming, parameters, response formats)
- Conversation Flow Principles (stateless request cycle, context building)
- Agent Behavior Constraints (tool selection, conversational guidelines)
- Frontend (ChatKit) Principles (configuration, message display, conversation management)
- Testing Requirements (MCP tools, agent integration, E2E)
- Development Workflow Standards (MCP server structure, agent integration pattern)
- Migration from Phase II (what changes, what stays same, backward compatibility)
- API Endpoints Summary (Phase II REST + Phase III Chat)
- Environment Variables (extended for AI/ChatKit)
- Non-Negotiables (8 AI-specific constraints)
- Quality Metrics (success metrics and UX metrics)
- Phase III-Specific Risks (risk matrix with mitigations)

**Database schema extensions defined:**
- Conversations table (id, user_id, timestamps)
- Messages table (id, user_id, conversation_id, role, content, tool_calls, created_at)
- Proper indexes on user_id and conversation_id

**Technology stack updated:**
- Added: OpenAI Agents SDK, Official Python MCP SDK, OpenAI ChatKit
- AI Model: gpt-4o-mini or gpt-4o (configurable)
- Forbidden: Custom chat UI, conversation state in memory, direct DB calls from agent

**Sync Impact Report:**
- Version: 2.0.0 → 3.0.0 (MAJOR - Phase III transition)
- No template updates required (all compatible)
- No follow-up TODOs

## Outcome

- ✅ Impact: Complete Phase III extension to constitution with AI chatbot capabilities via MCP
- 🧪 Tests: N/A - constitution document
- 📁 Files: .specify/memory/constitution.md (major extension, not replacement)
- 🔁 Next prompts: /sp.specify for Phase III feature spec, /sp.plan for implementation architecture
- 🧠 Reflection: MAJOR version bump justified - fundamental new architectural pattern (MCP tools + AI agents) while maintaining all Phase II principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation PASS - no unresolved placeholders, all principles declarative, Phase II fully preserved
- Prompt variant (if applicable): User-provided Phase III constitution content
- Next experiment: N/A
