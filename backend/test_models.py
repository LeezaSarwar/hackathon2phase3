#!/usr/bin/env python3
"""Test script to verify that the new models can be imported without issues."""

try:
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models import Conversation, Message
    
    print("✓ Successfully imported Conversation and Message models")
    
    # Test creating instances
    conv = Conversation(user_id="test_user")
    msg = Message(user_id="test_user", conversation_id=1, role="user", content="Hello")
    
    print("✓ Successfully created instances of Conversation and Message")
    print(f"Conversation user_id: {conv.user_id}")
    print(f"Message user_id: {msg.user_id}, role: {msg.role}, content: {msg.content}")
    
    print("\n✓ All tests passed! Models are properly structured.")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")