from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import re

from app.config import get_settings

settings = get_settings()

database_url = settings.database_url

# Remove sslmode from URL as it's handled in connect_args for asyncpg
if "sslmode=" in database_url:
    database_url = re.sub(r'[?&]sslmode=[^&]+', '', database_url)

if "postgresql" in database_url and "+asyncpg" not in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://")

# Create async engine with proper SSL handling for asyncpg
engine = create_async_engine(
    database_url,
    echo=False,
    future=True,
    connect_args={"ssl": "require"},
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
