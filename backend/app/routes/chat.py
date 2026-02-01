from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone
import traceback
import json

from app.database import get_session
from app.models import Task, Conversation, Message
from app.config import get_settings
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse, MessageResponse, ConversationResponse
from app.schemas.task import TaskCreate
from app.middleware.auth import get_current_user
from utils.agent import run_agent

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get chat history for the current user."""
    user_id = current_user.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")

    # Get the user's conversation (there should be only one)
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(1)
    )
    result = await session.execute(statement)
    conversation = result.scalar_one_or_none()

    if not conversation:
        # No conversation yet, return empty
        return ChatHistoryResponse(conversation=None, messages=[])

    # Get all messages for this conversation
    message_statement = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
    )
    message_result = await session.execute(message_statement)
    messages = message_result.scalars().all()

    return ChatHistoryResponse(
        conversation=ConversationResponse.model_validate(conversation),
        messages=[MessageResponse.model_validate(m) for m in messages]
    )


@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user_id = current_user.get("sub")
    print(f"DEBUG: Chat endpoint called by user_id: {user_id}")

    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")

    try:
        # Get or create conversation
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .limit(1)
        )
        result = await session.execute(statement)
        conversation = result.scalar_one_or_none()

        if not conversation:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            await session.flush()  # Get conversation.id

        # Build conversation history in the format expected by the agent
        conversation_history = []
        for m in request.messages:
            conversation_history.append({
                "role": m.role,
                "content": m.content
            })

        print(f"\n{'='*60}")
        print(f"CHAT ENDPOINT - Starting agent call")
        print(f"User ID: {user_id}")
        print(f"Conversation ID: {conversation.id}")
        print(f"Messages: {len(conversation_history)}")
        print(f"{'='*60}\n")

        # Run the agent with MCP tools
        agent_result = await run_agent(user_id, conversation_history, session)

        # Extract the response and tool calls
        response_content = agent_result["response"]
        tool_calls = agent_result["tool_calls"]

        # Log tool calls for debugging
        print(f"DEBUG: Agent executed {len(tool_calls)} tool calls")
        for i, tc in enumerate(tool_calls):
            print(f"  Tool {i+1}: {tc['name']} - {tc['result'].get('message', 'No message')}")

        # Save the user's message (last message in the request)
        if conversation_history:
            last_user_message = conversation_history[-1]
            if last_user_message["role"] == "user":
                user_message = Message(
                    user_id=user_id,
                    conversation_id=conversation.id,
                    role="user",
                    content=last_user_message["content"]
                )
                session.add(user_message)

        # Save the assistant's response
        assistant_message = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="assistant",
            content=response_content,
            tool_calls={"calls": tool_calls} if tool_calls else None
        )
        session.add(assistant_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.now(timezone.utc)

        print(f"\nCHAT ENDPOINT - About to commit session...")

        # Ensure all changes are committed to persist any changes made by the tools
        await session.commit()

        print(f"CHAT ENDPOINT - Session committed successfully!")

        # Return the agent's response
        return ChatResponse(content=response_content)

    except Exception as e:
        print(f"ERROR in chat_endpoint: {str(e)}")
        traceback.print_exc()
        # Rollback the session in case of error
        try:
            await session.rollback()
        except:
            pass  # Ignore rollback errors
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")
