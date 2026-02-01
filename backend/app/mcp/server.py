from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import json

# Import all 5 tools from mcp.tools
from .tools.add_task import add_task
from .tools.list_tasks import list_tasks
from .tools.complete_task import complete_task
from .tools.update_task import update_task
from .tools.delete_task import delete_task


def get_mcp_tools(user_id: str, session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Returns list of tool definitions in OpenAI function calling format.
    
    Args:
        user_id: The ID of the user requesting the tools
        session: Database session
    
    Returns:
        List of tool definitions in OpenAI function calling format
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional description of the task"
                        }
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Query tasks from the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter tasks by status (default: all)"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to mark as complete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "The new title for the task (optional)"
                        },
                        "description": {
                            "type": "string",
                            "description": "The new description for the task (optional)"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task from the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to delete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]
    
    return tools


async def execute_mcp_tool(tool_name: str, tool_args: Dict[str, Any], user_id: str, session: AsyncSession) -> Dict[str, Any]:
    """
    Routes tool calls to correct tool function.

    Args:
        tool_name: Name of the tool to execute
        tool_args: Arguments for the tool
        user_id: The ID of the user executing the tool
        session: Database session

    Returns:
        Result from the executed tool
    """
    try:
        logging.info(f"Executing tool: {tool_name} for user: {user_id}")
        logging.info(f"Tool arguments: {json.dumps(tool_args)}")

        # Add user_id and session to tool_args
        tool_args_with_context = tool_args.copy()
        tool_args_with_context["user_id"] = user_id
        tool_args_with_context["session"] = session

        # Route to the correct tool function
        if tool_name == "general_response":
            # For general conversation, just return the message
            return {
                "success": True,
                "data": {"message": tool_args.get("message", "")},
                "message": tool_args.get("message", "")
            }
        elif tool_name == "add_task":
            result = await add_task(**tool_args_with_context)
        elif tool_name == "list_tasks":
            result = await list_tasks(**tool_args_with_context)
        elif tool_name == "complete_task":
            result = await complete_task(**tool_args_with_context)
        elif tool_name == "update_task":
            result = await update_task(**tool_args_with_context)
        elif tool_name == "delete_task":
            result = await delete_task(**tool_args_with_context)
        else:
            logging.error(f"Unknown tool: {tool_name}")
            return {
                "success": False,
                "data": {},
                "message": f"Unknown tool: {tool_name}"
            }

        logging.info(f"Tool {tool_name} executed successfully")
        return result

    except Exception as e:
        logging.error(f"Error executing tool {tool_name}: {str(e)}")
        return {
            "success": False,
            "data": {},
            "message": f"Error executing tool {tool_name}: {str(e)}"
        }