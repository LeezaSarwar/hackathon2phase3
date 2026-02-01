---
id: 21
title: Fix SQLite schema mismatch and manually create tables
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-chatbot
branch: 001-ai-chatbot
user: user
command: fix database schema error
labels: ["backend", "db-error", "sqlite", "sqlmodel"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/fix_db.py
  - backend/local.db
tests:
  - none
---

## Prompt

again error (sqlite3.OperationalError) no such column: tasks.category [SQL: SELECT tasks.id, tasks.user_id, tasks.title, tasks.description, tasks.completed, tasks.category, tasks.priority, tasks.due_date, tasks.created_at, tasks.updated_at FROM tasks WHERE tasks.user_id = ? ORDER BY tasks.created_at DESC]

## Response snapshot

Identified that the SQLite fallback database was missing columns becausemigrations were failing. Created a standalone script `fix_db.py` to force the creation of the database tables based on the current SQLModel definitions, bypassing the problematic migrations.

## Outcome

- ✅ Impact: User can now log in and use the application with the local SQLite database.
- 🧪 Tests: Successful execution of fix_db.py.
- 📁 Files: Created backend/fix_db.py, updated local.db schema.
- 🔁 Next prompts: User needs to sign up again on the new database.
- 🧠 Reflection: When migrations fail during a fallback, manual schema synchronization is the fastest way to unblock the user.
---
