from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.task import Task


async def add_task(user_id: str, title: str, description: Optional[str] = None, session: AsyncSession = None):
    """
    Create a task in the database.

    Args:
        user_id: The ID of the user creating the task
        title: The title of the task
        description: Optional description of the task
        session: Database session

    Returns:
        Dict with success status, data, and message
    """
    try:
        print(f"Adding task for user_id: {user_id}, title: {title}")

        # Create a new task instance - let the model handle created_at and updated_at
        task = Task(
            user_id=user_id,
            title=title,
            description=description
        )

        # Add the task to the session
        session.add(task)

        # Commit the changes to the database
        await session.commit()

        # Refresh the task to get the generated ID and updated timestamps
        await session.refresh(task)

        print(f"Task created successfully with ID: {task.id}")

        return {
            "success": True,
            "data": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "category": task.category,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            },
            "message": "Task created successfully"
        }

    except Exception as e:
        print(f"Error adding task: {str(e)}")
        return {
            "success": False,
            "data": {},
            "message": f"Error adding task: {str(e)}"
        }