from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.task import Task


async def list_tasks(user_id: str, status: str = "all", session: AsyncSession = None):
    """
    Query tasks from the database.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        status: Filter tasks by status ('all', 'pending', 'completed')
        session: Database session

    Returns:
        Dict with success status, data, and message
    """
    try:
        print(f"Listing tasks for user_id: {user_id}, status: {status}")

        # Build the query based on the status filter
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        # For "all", no additional filter is needed

        # Execute the query asynchronously
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Convert tasks to dictionaries
        tasks_data = []
        for task in tasks:
            task_dict = {
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
            }
            tasks_data.append(task_dict)

        print(f"Found {len(tasks_data)} tasks for user_id: {user_id}")

        return {
            "success": True,
            "data": {
                "tasks": tasks_data,
                "count": len(tasks_data)
            },
            "message": f"Successfully retrieved {len(tasks_data)} tasks"
        }

    except Exception as e:
        print(f"Error listing tasks: {str(e)}")
        return {
            "success": False,
            "data": {
                "tasks": [],
                "count": 0
            },
            "message": f"Error listing tasks: {str(e)}"
        }