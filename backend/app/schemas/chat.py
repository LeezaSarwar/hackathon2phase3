from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    conversation: Optional[ConversationResponse]
    messages: List[MessageResponse]
