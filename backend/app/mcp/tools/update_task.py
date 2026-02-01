from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from datetime import datetime, timezone


def utcnow():
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    session: AsyncSession = None
):
    """
    Update task details.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: Optional new title for the task
        description: Optional new description for the task
        session: Database session

    Returns:
        Dict with success status, data, and message
    """
    try:
        print(f"Updating task for user_id: {user_id}, task_id: {task_id}")

        # Query the task by user_id and task_id to ensure ownership
        query = select(Task).where(Task.user_id == user_id).where(Task.id == task_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            print(f"Task with id {task_id} not found for user {user_id}")
            return {
                "success": False,
                "data": {},
                "message": "Task not found or user does not have permission to modify this task"
            }

        # Update the task fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        # Update the updated_at timestamp
        task.updated_at = utcnow()

        # Flush to persist changes without committing
        await session.flush()
        await session.refresh(task)

        print(f"Task {task_id} updated successfully")

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
            "message": "Task updated successfully"
        }

    except Exception as e:
        print(f"Error updating task: {str(e)}")
        return {
            "success": False,
            "data": {},
            "message": f"Error updating task: {str(e)}"
        }