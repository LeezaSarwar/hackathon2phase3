from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.types import JSON
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any


def utcnow():
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class Message(SQLModel, table=True):
    """Message model representing a message in a conversation."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, foreign_key="users.id")  # Foreign key to users table
    conversation_id: int = Field(index=True, nullable=False, foreign_key="conversations.id")  # Foreign key to conversations table
    role: str = Field(max_length=20, nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False)  # Message content
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON, nullable=True))  # JSON field for tool calls
    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")