#!/usr/bin/env python3
"""
Debug script to test database connectivity and task operations.
Run this to verify the database is working properly.
"""
import asyncio
import sys
import os
import re

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from app.config import get_settings
from app.models import Task, User


async def test_database():
    settings = get_settings()
    original_url = settings.database_url
    print(f"Original database URL: {original_url}")

    # Clean URL for asyncpg - remove sslmode from URL
    clean_url = original_url
    if "sslmode=" in clean_url:
        clean_url = re.sub(r'[?&]sslmode=[^&]+', '', clean_url)

    # Add asyncpg prefix
    if "postgresql://" in clean_url and "+asyncpg" not in clean_url:
        clean_url = clean_url.replace("postgresql://", "postgresql+asyncpg://")
    elif "postgres://" in clean_url and "+asyncpg" not in clean_url:
        clean_url = clean_url.replace("postgres://", "postgresql+asyncpg://")

    print(f"Async URL for testing: {clean_url}")

    # Create async engine with proper SSL handling
    engine = create_async_engine(
        clean_url,
        echo=True,
        connect_args={"ssl": "require"}
    )

    try:
        async with engine.connect() as conn:
            # Test connection
            print("\n1. Testing database connection...")
            result = await conn.execute(text("SELECT 1"))
            print("   Connection successful!")

            # Check if tables exist
            print("\n2. Checking if tables exist...")
            result = await conn.execute(text("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"   Tables found: {tables}")

            # Create tables using SQLModel metadata
            if 'users' not in tables or 'tasks' not in tables:
                print("\n3. Creating tables using SQLModel...")
                # For async, we need to use the sync method
                await conn.run_sync(SQLModel.metadata.create_all)
                print("   Tables created!")
                # Refresh tables list
                result = await conn.execute(text("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'
                """))
                tables = [row[0] for row in result.fetchall()]
                print(f"   Tables now: {tables}")

            # Check existing users
            print("\n4. Checking existing users...")
            result = await conn.execute(text("SELECT id, email FROM users LIMIT 5"))
            users = result.fetchall()
            print(f"   Found {len(users)} users")
            for user in users:
                print(f"   - {user[1]} (id: {user[0]})")

            # Create a test task if we have users
            if users:
                test_user_id = users[0][0]
                print(f"\n5. Creating test task for user {test_user_id}...")

                # Check for existing tasks
                result = await conn.execute(
                    text("SELECT COUNT(*) FROM tasks WHERE user_id = :user_id"),
                    {"user_id": test_user_id}
                )
                count = result.scalar()
                print(f"   User already has {count} tasks")

                # Use raw SQL for async insert
                result = await conn.execute(
                    text("""
                        INSERT INTO tasks (user_id, title, description, category, priority)
                        VALUES (:user_id, :title, :description, :category, :priority)
                        RETURNING id
                    """),
                    {
                        "user_id": test_user_id,
                        "title": "Debug Test Task",
                        "description": "This task was created by the debug script",
                        "category": "Personal",
                        "priority": "Medium"
                    }
                )
                new_id = result.scalar()
                await conn.commit()
                print(f"   Test task created with ID: {new_id}!")

                # Verify
                result = await conn.execute(
                    text("SELECT id, title, completed FROM tasks WHERE user_id = :user_id ORDER BY id DESC LIMIT 5"),
                    {"user_id": test_user_id}
                )
                tasks = result.fetchall()
                print(f"\n6. User's tasks after test:")
                for t in tasks:
                    print(f"   - ID: {t[0]}, Title: {t[1]}, Completed: {t[2]}")
            else:
                print("\n5. No users found - cannot create test task")

        print("\nDatabase test completed successfully!")
        return True

    except Exception as e:
        print(f"\nDatabase test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await engine.dispose()


if __name__ == "__main__":
    success = asyncio.run(test_database())
    sys.exit(0 if success else 1)

