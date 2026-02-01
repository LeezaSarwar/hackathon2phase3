"""add_chat_tables

Revision ID: 003
Revises: 9f6aa00b8851
Create Date: 2026-01-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '9f6aa00b8851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create index on user_id for fast lookups
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )

    # Create indexes for better query performance
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_user_id', 'messages', ['user_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_messages_created_at')
    op.drop_index('idx_messages_user_id')
    op.drop_index('idx_messages_conversation_id')

    # Drop messages table
    op.drop_table('messages')

    # Drop conversations index and table
    op.drop_index('idx_conversations_user_id')
    op.drop_table('conversations')
