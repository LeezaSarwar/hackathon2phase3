# 🤖 Phase III: AI-Powered Todo Chatbot

[![Phase](https://img.shields.io/badge/Phase-III-blue.svg)](https://github.com/yourusername/hackathon-todo)
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)](https://github.com/yourusername/hackathon-todo)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Hackathon II - The Evolution of Todo**  
> Transforming traditional task management into an intelligent conversational experience using AI agents and MCP tools.


## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [MCP Tools](#mcp-tools)
- [Screenshots](#screenshots)
- [Demo Video](#demo-video)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)
- [Acknowledgments](#acknowledgments)
- [License](#license)

---

## 🎯 Overview

Phase III introduces **conversational AI capabilities** to the Todo application, allowing users to manage their tasks through natural language interactions. Built with OpenAI's GPT-4o-mini and Model Context Protocol (MCP), the chatbot understands user intent and performs actual database operations.

### 🌟 What Makes This Special?

- **Natural Language Interface**: Talk to your todo list like you would to a personal assistant
- **Real-Time Database Operations**: All changes persist immediately to Neon PostgreSQL
- **Stateless Architecture**: Server-side implementation that scales horizontally
- **MCP Integration**: Standardized protocol for AI-to-database communication
- **Conversation Persistence**: Full chat history maintained across sessions

---

## ✨ Features

### Phase III Core Features

#### 🗣️ Conversational Task Management
- **Natural Language Processing**: Understand commands like "Add groceries to my list" or "Show me pending tasks"
- **Context-Aware Responses**: AI remembers conversation flow and provides relevant responses
- **Action Confirmation**: Friendly confirmations after each operation with specific details

#### 🔧 MCP Tools Implementation
Five production-ready tools for task operations:

1. **`add_task`** - Create new tasks in database
2. **`list_tasks`** - Query and filter tasks (all/pending/completed)
3. **`complete_task`** - Mark tasks as complete
4. **`update_task`** - Modify task title and description
5. **`delete_task`** - Remove tasks with confirmation

#### 💾 Stateless Server Design
- Full conversation history loaded from database on each request
- No in-memory session storage
- Horizontal scalability ready
- Server restarts don't lose data

#### 🔐 Security & Authorization
- JWT-based authentication (Better Auth)
- User isolation - each user sees only their tasks
- Tool-level authorization checks
- Secure API key management

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **UI Library**: OpenAI ChatKit
- **Authentication**: Better Auth with JWT
- **Styling**: Tailwind CSS
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **AI Integration**: OpenAI Agents SDK
- **MCP**: Official Python MCP SDK
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth JWT verification

### AI & Tools
- **Model**: GPT-4o-mini (OpenAI)
- **Protocol**: Model Context Protocol (MCP)
- **Function Calling**: OpenAI Function Calling API

### DevOps
- **Package Manager**: UV (Python), npm (JavaScript)
- **Development**: Hot reload with Uvicorn
- **Deployment**: Vercel (Frontend), Railway/Render (Backend)

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         OpenAI ChatKit (Conversational UI)               │  │
│  │                                                          │  │
│  │  User types: "Add task to buy groceries"                │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │ POST /api/{user_id}/chat          │
└───────────────────────────┼─────────────────────────────────────┘
                            │ + JWT Token
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Chat Endpoint (Stateless)                   │  │
│  │  1. Load conversation history from database              │  │
│  │  2. Store user message                                   │  │
│  │  3. Run OpenAI agent with MCP tools                      │  │
│  │  4. Store assistant response                             │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                    │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │         OpenAI Agents SDK Integration                    │  │
│  │  - Understands natural language                          │  │
│  │  - Selects appropriate MCP tool                          │  │
│  │  - Extracts parameters from user message                 │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                    │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │              MCP Server (Tool Router)                    │  │
│  │                                                          │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐      │  │
│  │  │add_task  │  │list_tasks│  │complete_task     │      │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘      │  │
│  │  ┌──────────┐  ┌──────────┐                            │  │
│  │  │update_   │  │delete_   │                            │  │
│  │  │task      │  │task      │                            │  │
│  │  └──────────┘  └──────────┘                            │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │ SQLModel Queries                  │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              NEON SERVERLESS POSTGRESQL                         │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌───────────┐  │
│  │  users   │  │  tasks   │  │conversations │  │ messages  │  │
│  │(Phase II)│  │(Phase II)│  │ (Phase III)  │  │(Phase III)│  │
│  └──────────┘  └──────────┘  └──────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Request Flow: "Add Groceries"

1. **User Input**: Types "Add a task to buy groceries" in chatbot
2. **Frontend**: ChatKit sends POST request with JWT token
3. **Backend Endpoint**: Authenticates user, loads conversation history
4. **Agent Processing**: OpenAI analyzes intent → selects `add_task` tool
5. **MCP Execution**: `add_task` tool creates Task in database
6. **Database**: Task persisted to Neon PostgreSQL
7. **Response Chain**: Success → Agent → Endpoint → ChatKit
8. **User Sees**: "✓ Added 'buy groceries' to your list (ID: 42)"

---

## 🚀 Installation

### Prerequisites

- **Node.js** 20+
- **Python** 3.13+
- **UV** package manager ([Install UV](https://github.com/astral-sh/uv))
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Neon Account** ([Sign up](https://neon.tech))

### Clone Repository

```bash
git clone https://github.com/yourusername/hackathon-todo.git
cd hackathon-todo
```

### Backend Setup

```bash
cd backend

# Install dependencies with UV
uv sync

# Or using pip
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
# or
pnpm install
```

---

## ⚙️ Environment Setup

### Backend Environment Variables

Create `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@your-neon-host/dbname?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here

# OpenAI (Phase III)
OPENAI_API_KEY=sk-your-openai-api-key-here
AGENT_MODEL=gpt-4o-mini

# Server Configuration
CORS_ORIGINS=http://localhost:3000
```

### Frontend Environment Variables

Create `frontend/.env.local`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000

# OpenAI ChatKit (Phase III)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=odkey-your-domain-key-here
```

### Database Migration

```bash
cd backend

# Run migrations to create conversations and messages tables
uv run alembic upgrade head

# Or manually create tables using provided SQL
psql $DATABASE_URL < migrations/003_add_conversations.sql
```

---

## 💻 Usage

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Using the Chatbot

1. **Sign Up/Sign In** at `/signin` or `/signup`
2. Navigate to **Chat Assistant** tab
3. Start conversing:

```
You: Add a task to buy groceries
Bot: ✓ Added 'buy groceries' to your list (ID: 42)

You: Show me all my tasks
Bot: Here are your tasks:
     1. Buy groceries (pending) - ID: 42
     You have 1 task.

You: Mark task 42 as complete
Bot: Great! Marked 'buy groceries' as complete.

You: What's left to do?
Bot: You have no pending tasks. All caught up! 🎉
```

---

## 📚 API Documentation

### Chat Endpoint

#### POST `/api/{user_id}/chat`

Send a message to the AI chatbot.

**Request:**
```json
{
  "conversation_id": 1,  // Optional - creates new if omitted
  "message": "Add a task to buy milk"
}
```

**Response:**
```json
{
  "conversation_id": 1,
  "response": "✓ Added 'buy milk' to your list (ID: 5)",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {"title": "buy milk"},
      "result": {"success": true, "task_id": 5}
    }
  ]
}
```

### Conversation Management

#### GET `/api/{user_id}/conversations`
List all user's conversations.

#### GET `/api/{user_id}/conversations/{id}`
Get full conversation history with messages.

#### DELETE `/api/{user_id}/conversations/{id}`
Delete a conversation and all its messages.

---

## 🔧 MCP Tools

### Tool 1: add_task

**Purpose**: Create a new task in the database

**Parameters:**
- `title` (string, required): Task title (1-200 chars)
- `description` (string, optional): Additional details

**Example:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Returns:**
```json
{
  "success": true,
  "data": {
    "task_id": 42,
    "title": "Buy groceries",
    "status": "created"
  },
  "message": "Task 'Buy groceries' added successfully"
}
```

### Tool 2: list_tasks

**Purpose**: Query tasks from database

**Parameters:**
- `status` (enum, optional): "all" | "pending" | "completed"

**Returns:**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 42,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "created_at": "2025-12-29T10:30:00Z"
      }
    ],
    "count": 1
  },
  "message": "Retrieved 1 task from database"
}
```

### Tool 3: complete_task

**Purpose**: Mark a task as complete

**Parameters:**
- `task_id` (integer, required): ID of task to complete

### Tool 4: update_task

**Purpose**: Update task details

**Parameters:**
- `task_id` (integer, required)
- `title` (string, optional)
- `description` (string, optional)

### Tool 5: delete_task

**Purpose**: Delete a task from database

**Parameters:**
- `task_id` (integer, required)

---

## 📸 Screenshots

### Chatbot Interface
![Chatbot Interface](./screenshots/chatbot-ui.png)
*Natural language task management with OpenAI ChatKit*

### Task Management
![Task List](./screenshots/task-list.png)
*Tasks added via chatbot appear on the /tasks page*

### Conversation History
![Conversation](./screenshots/conversation.png)
*Full conversation history with tool calls*

---

## 🎥 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://youtube.com/watch?v=YOUR_VIDEO_ID)

**Duration**: 90 seconds  
**Highlights**:
- Conversational task creation
- Natural language queries
- Real-time database operations
- Multi-turn conversation flow
- Task persistence verification

[🔗 Watch on YouTube](https://youtube.com/watch?v=YOUR_VIDEO_ID)

---

## 🧩 Challenges & Solutions

### Challenge 1: Agent Not Calling MCP Tools

**Problem**: OpenAI agent was responding with text but not executing tools.

**Solution**:
- Made agent instructions explicit about tool usage
- Added `tool_choice="auto"` with clear descriptions
- Implemented extensive logging to debug tool selection
- Forced lower temperature (0.3) for more deterministic behavior

### Challenge 2: Database Session Not Persisting

**Problem**: Tools were being called but changes weren't saving to database.

**Solution**:
- Verified session flow: endpoint → agent → MCP server → tools
- Added session ID logging to trace the same session object
- Ensured `session.commit()` was called in every tool
- Used FastAPI's `Depends(get_session)` properly

### Challenge 3: Stateless Architecture Implementation

**Problem**: Maintaining conversation context without server-side memory.

**Solution**:
- Store all messages in PostgreSQL immediately
- Load full history from database on each request
- Pass conversation context to agent every time
- Server holds zero state between requests

### Challenge 4: OpenAI Function Calling Reliability

**Problem**: Agent sometimes ignored tools or used them incorrectly.

**Solution**:
- Clear, action-oriented tool descriptions
- Strict parameter schemas with examples
- Agent instructions emphasizing tool priority
- Regular testing with edge cases

---

## 🚀 Future Enhancements

### Phase IV Additions (Planned)
- [ ] Local Kubernetes deployment with Minikube
- [ ] Helm charts for container orchestration
- [ ] kubectl-ai and kagent integration
- [ ] Docker containerization with Gordon

### Phase V Additions (Planned)
- [ ] Advanced features: priorities, tags, due dates
- [ ] Event-driven architecture with Kafka
- [ ] Dapr for distributed application runtime
- [ ] Cloud deployment (GKE/AKS/OKE)
- [ ] CI/CD pipeline with GitHub Actions

### Additional Features
- [ ] Voice input support
- [ ] Multi-language support (Urdu)
- [ ] Task collaboration (shared lists)
- [ ] Calendar integration
- [ ] Mobile app (React Native)

---

## 🙏 Acknowledgments

### Hackathon Organizers
- **Panaversity Team**: For organizing this amazing learning experience
- **PIAIC & GIAIC**: For the opportunity and guidance
- **Instructors**: Zia Khan, Rehan, Junaid, and Wania

### Technologies Used
- **OpenAI**: For GPT-4o-mini and ChatKit
- **Anthropic**: For Claude Code assistance in development
- **Neon**: For serverless PostgreSQL database
- **Vercel**: For seamless frontend deployment
- **FastAPI Team**: For the amazing Python framework

### Resources
- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/guides/agents)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

- **Developer**: [LeezaSarwar]  
- **Email**: leezasarwar0@gmail.com  
- **GitHub**: [@LeezaSarwar](https://github.com/LeezaSarwar)  
- **LinkedIn**: [leeza-sarwar](https://linkedin.com/in/leeza-sarwar)  
- **Portfolio**: [LeezaSarwar](https://leezasarwar.techkl.de)
- **X**: [LeezaSarwar](https://x.com/LeezaSarwar)

---

## 🌟 Star This Repository

If you found this project helpful or interesting, please give it a ⭐!

---

**Built with ❤️ for Panaversity Hackathon II**

*Transforming task management through conversational AI* 🤖✨
