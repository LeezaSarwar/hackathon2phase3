from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone
from typing import Optional, List


def utcnow():
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class Conversation(SQLModel, table=True):
    """Conversation model representing a chat conversation."""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, foreign_key="users.id")  # Foreign key to users table
    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")