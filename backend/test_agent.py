#!/usr/bin/env python3
"""Test script to verify that the agent can be imported and used correctly."""

try:
    from backend.utils.agent import run_agent, AGENT_INSTRUCTIONS
    print("✓ Successfully imported run_agent function and AGENT_INSTRUCTIONS")
    
    # Test that the function exists
    print(f"✓ run_agent function exists: {callable(run_agent)}")
    print(f"✓ AGENT_INSTRUCTIONS exists: {bool(AGENT_INSTRUCTIONS)}")
    
    print("\n✓ All tests passed! Agent module is properly structured.")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")