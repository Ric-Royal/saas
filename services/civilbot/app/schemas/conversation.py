from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime
from app.models.models import IntentEnum

class MessageBase(BaseModel):
    content: str
    is_bot: bool = False
    intent: Optional[IntentEnum] = None
    confidence_score: Optional[int] = None
    metadata: Optional[Dict] = None

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    translated_content: Optional[Dict] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    user_id: int
    context: Optional[Dict] = None
    intent: Optional[IntentEnum] = None
    sentiment_score: Optional[int] = None
    is_active: bool = True
    metadata: Optional[Dict] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    user_id: Optional[int] = None
    context: Optional[Dict] = None
    intent: Optional[IntentEnum] = None
    sentiment_score: Optional[int] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict] = None

class Conversation(ConversationBase):
    id: int
    last_interaction: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[Message] = []

    class Config:
        from_attributes = True 