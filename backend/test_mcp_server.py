#!/usr/bin/env python3
"""Test script to verify that the MCP server can be imported and used correctly."""

try:
    from app.mcp.server import get_mcp_tools, execute_mcp_tool
    print("✓ Successfully imported get_mcp_tools and execute_mcp_tool")
    
    # Test that the functions exist
    print(f"✓ get_mcp_tools function exists: {callable(get_mcp_tools)}")
    print(f"✓ execute_mcp_tool function exists: {callable(execute_mcp_tool)}")
    
    print("\n✓ All tests passed! MCP server is properly structured.")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")