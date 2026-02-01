from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task


async def delete_task(user_id: str, task_id: int, session: AsyncSession = None):
    """
    Delete a task from the database.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete
        session: Database session

    Returns:
        Dict with success status, data, and message
    """
    try:
        print(f"Deleting task for user_id: {user_id}, task_id: {task_id}")

        # Query the task by user_id and task_id to ensure ownership
        query = select(Task).where(Task.user_id == user_id).where(Task.id == task_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            print(f"Task with id {task_id} not found for user {user_id}")
            return {
                "success": False,
                "data": {},
                "message": "Task not found or user does not have permission to delete this task"
            }

        # Delete the task from the session
        session.delete(task)

        # Flush to persist changes without committing
        await session.flush()

        print(f"Task {task_id} deleted successfully")

        return {
            "success": True,
            "data": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title
            },
            "message": "Task deleted successfully"
        }

    except Exception as e:
        print(f"Error deleting task: {str(e)}")
        return {
            "success": False,
            "data": {},
            "message": f"Error deleting task: {str(e)}"
        }