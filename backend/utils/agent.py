import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session

# Import Google GenAI client
try:
    from google import genai
    from google.genai import types
except ImportError:
    raise ImportError("Please install the google-genai package: pip install google-genai")

# Import configuration
from app.config import get_settings

# Import MCP tools functions
from app.mcp.server import get_mcp_tools, execute_mcp_tool


# Define agent instructions with conversational personality
AGENT_INSTRUCTIONS = """
You are a helpful and friendly task management assistant. Your personality is:
- Friendly and conversational
- Helpful and supportive
- Professional but approachable
- Detail-oriented and organized

CRITICAL INSTRUCTIONS - YOU MUST FOLLOW THESE:
1. When a user asks you to add, update, complete, or list tasks, IMMEDIATELY call the appropriate tool function
2. DO NOT ask for permission or confirmation before calling tools (except for delete operations)
3. DO NOT just say you will do something - ACTUALLY CALL THE TOOL FUNCTION
4. After calling a tool, tell the user what you did based on the tool's response

Your responsibilities:
- Help users manage their tasks effectively by CALLING THE APPROPRIATE TOOLS
- When users ask to add a task, IMMEDIATELY call add_task with the title and description
- When users ask to list tasks, IMMEDIATELY call list_tasks
- When users ask to update a task, IMMEDIATELY call update_task with the task_id and new values
- When users ask to complete a task, IMMEDIATELY call complete_task with the task_id
- When users ask to delete a task, first confirm with the user, then call delete_task

When displaying tasks:
- Use clear formatting with titles, descriptions, and status
- Group tasks logically (pending vs completed)
- Use bullet points or numbered lists for readability

Available tools (YOU MUST USE THESE):
- add_task: Create a new task (call this immediately when user wants to add a task)
- list_tasks: View existing tasks (call this immediately when user wants to see tasks)
- complete_task: Mark a task as complete (call this immediately when user wants to complete a task)
- update_task: Modify task details (call this immediately when user wants to update a task)
- delete_task: Remove a task (ask for confirmation first, then call this)

REMEMBER: You have function calling capabilities. USE THEM. Don't just talk about using tools - actually call them!
"""


def create_gemini_tools():
    """Create the tools list for Gemini."""
    # Define the tools in the format expected by the Gemini API
    tools = [
        {
            "function_declarations": [
                {
                    "name": "add_task",
                    "description": "IMMEDIATELY call this function to create and save a new task to the database when the user wants to add a task. This function will persist the task to the database.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task (required)",
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional detailed description of the task",
                            },
                        },
                        "required": ["title"],
                    },
                },
                {
                    "name": "list_tasks",
                    "description": "IMMEDIATELY call this function to retrieve and display all tasks from the database when the user wants to see their tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Filter tasks by status (default: all)",
                            },
                        },
                    },
                },
                {
                    "name": "complete_task",
                    "description": "IMMEDIATELY call this function to mark a task as completed in the database when the user wants to complete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The unique integer ID of the task to mark as complete",
                            },
                        },
                        "required": ["task_id"],
                    },
                },
                {
                    "name": "update_task",
                    "description": "IMMEDIATELY call this function to update and save task details in the database when the user wants to modify a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The unique integer ID of the task to update",
                            },
                            "title": {
                                "type": "string",
                                "description": "The new title for the task (optional)",
                            },
                            "description": {
                                "type": "string",
                                "description": "The new description for the task (optional)",
                            },
                        },
                        "required": ["task_id"],
                    },
                },
                {
                    "name": "delete_task",
                    "description": "IMMEDIATELY call this function to permanently delete a task from the database when the user confirms they want to delete it",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The unique integer ID of the task to delete",
                            },
                        },
                        "required": ["task_id"],
                    },
                }
            ]
        }
    ]
    return tools


async def run_agent(user_id: str, messages: List[Dict[str, str]], session: AsyncSession) -> Dict[str, Any]:
    """
    Run the Google Gemini agent to process user messages and interact with task management tools.
    
    Args:
        user_id: The ID of the user interacting with the agent
        messages: List of conversation messages in OpenAI format
        session: Database session for database operations
    
    Returns:
        Dict with response string and list of tool calls made
    """
    try:
        logging.info(f"Running agent for user: {user_id}")
        
        # Get settings
        settings = get_settings()

        # Initialize Google GenAI client
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key not configured")

        client = genai.Client(api_key=settings.gemini_api_key)

        # Get available tools for Gemini
        tools = create_gemini_tools()

        # Prepare the messages for Gemini
        contents = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

        # Configure the generation with automatic function calling
        # Strong instructions will guide the model to call functions
        config = types.GenerateContentConfig(
            system_instruction=AGENT_INSTRUCTIONS,
            tools=tools,
        )

        # Initial generation
        logging.debug(f"Calling Gemini with model {settings.agent_model}")
        print(f"\n{'='*60}")
        print(f"🤖 AGENT - Calling Gemini API")
        print(f"Model: {settings.agent_model}")
        print(f"Tools available: {len(tools)}")
        print(f"Messages in conversation: {len(contents)}")
        print(f"{'='*60}\n")

        response = await client.aio.models.generate_content(
            model=settings.agent_model,
            contents=contents,
            config=config
        )
        logging.debug("Gemini initial response received")

        print(f"\n{'='*60}")
        print(f"📥 AGENT - Gemini response received")
        print(f"Candidates: {len(response.candidates) if response.candidates else 0}")
        print(f"{'='*60}\n")

        # Handle tool calls in a loop
        max_turns = 5
        turn_count = 0
        tool_calls_executed = []

        while max_turns > 0:
            turn_count += 1
            candidate = response.candidates[0] if response.candidates else None
            content = candidate.content if candidate else None
            parts = content.parts if content and hasattr(content, 'parts') and content.parts else []

            if not parts:
                logging.debug(f"Turn {turn_count} - No candidates or parts (candidate={bool(candidate)})")
                break

            # Find function calls in the current response
            function_calls = [p.function_call for p in parts if p.function_call]
            logging.debug(f"Turn {turn_count} - Gemini function calls found: {len(function_calls)}")

            print(f"\n{'='*60}")
            print(f"🔍 AGENT - Turn {turn_count}")
            print(f"Parts in response: {len(parts)}")
            print(f"Function calls detected: {len(function_calls)}")
            if function_calls:
                for fc in function_calls:
                    print(f"  - Function: {fc.name}")
                    print(f"    Args: {fc.args}")
            else:
                # Check if there's text instead
                text_parts = [p.text for p in parts if hasattr(p, 'text') and p.text]
                if text_parts:
                    print(f"  - Text response (no function call): {text_parts[0][:100]}...")
            print(f"{'='*60}\n")

            if not function_calls:
                response_text = content.parts[0].text if content and content.parts and content.parts[0].text else "I couldn't take any actions."
                return {
                    "response": response_text,
                    "tool_calls": tool_calls_executed
                }

            contents.append(content)
            tool_results = []

            for fc in function_calls:
                print(f"\n{'='*50}")
                print(f"EXECUTING TOOL: {fc.name}")
                print(f"ARGS: {fc.args}")
                print(f"USER_ID: {user_id}")
                print(f"SESSION: {session}")
                print(f"{'='*50}\n")

                res_data = None
                try:
                    # Execute the tool using our MCP tools
                    result = await execute_mcp_tool(fc.name, fc.args, user_id, session)

                    # Add to executed tool calls
                    tool_calls_executed.append({
                        "name": fc.name,
                        "arguments": fc.args,
                        "result": result
                    })

                    # Use the result data for the response
                    res_data = result.get("data", {"status": "executed"})

                    print(f"✅ Tool {fc.name} SUCCESS: {result}")
                    logging.info(f"Tool {fc.name} result: {res_data}")

                except Exception as tool_err:
                    print(f"❌ Tool {fc.name} FAILED: {str(tool_err)}")
                    logging.error(f"ERROR executing tool {fc.name}: {str(tool_err)}")
                    res_data = {"error": f"{fc.name} failed: {str(tool_err)}"}

                tool_results.append(types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response=res_data
                    )
                ))

            # Send results back to Gemini
            contents.append(types.Content(role="user", parts=tool_results))
            response = await client.aio.models.generate_content(
                model=settings.agent_model,
                contents=contents,
                config=config
            )
            max_turns -= 1

        final_content = response.text or "Done."
        logging.info(f"Agent response generated for user: {user_id}")

        return {
            "response": final_content,
            "tool_calls": tool_calls_executed
        }

    except Exception as e:
        logging.error(f"Error running agent for user {user_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"\n{'='*60}")
        print(f"❌ AGENT ERROR")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"{'='*60}\n")
        return {
            "response": "I'm sorry, I encountered an error while processing your request. Please try again.",
            "tool_calls": []
        }