from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from datetime import datetime, timezone


def utcnow():
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


async def complete_task(user_id: str, task_id: int, session: AsyncSession = None):
    """
    Mark a task as complete.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to mark as complete
        session: Database session

    Returns:
        Dict with success status, data, and message
    """
    try:
        print(f"Completing task for user_id: {user_id}, task_id: {task_id}")

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

        # Update the task's completed status
        task.completed = True
        task.updated_at = utcnow()

        # Flush to persist changes without committing
        await session.flush()
        await session.refresh(task)

        print(f"Task {task_id} marked as complete successfully")

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
            "message": "Task marked as complete successfully"
        }

    except Exception as e:
        print(f"Error completing task: {str(e)}")
        return {
            "success": False,
            "data": {},
            "message": f"Error completing task: {str(e)}"
        }