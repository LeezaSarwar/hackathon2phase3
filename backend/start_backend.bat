@echo off
set GEMINI_API_KEY=AIzaSyBftZdwXxtooXuKbbu7I63JItkZv0DEkYg
set AGENT_MODEL=models/gemini-flash-lite-latest
set MAX_CONVERSATION_MESSAGES=50
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
