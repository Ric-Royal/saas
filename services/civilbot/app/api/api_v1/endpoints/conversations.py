from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.crud import crud_conversation
from app.schemas.conversation import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
    Message,
    MessageCreate
)
from app.core.security import verify_admin_token
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[Conversation])
def list_conversations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    admin: bool = Depends(verify_admin_token)
):
    """
    List conversations with optional filters
    """
    filters = {
        "user_id": user_id,
        "is_active": is_active,
        "start_date": start_date,
        "end_date": end_date
    }
    conversations = crud_conversation.get_multi_with_filters(
        db, skip=skip, limit=limit, filters=filters
    )
    return conversations

@router.get("/{conversation_id}", response_model=Conversation)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(deps.get_db),
    admin: bool = Depends(verify_admin_token)
):
    """
    Get specific conversation by ID
    """
    conversation = crud_conversation.get(db, id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/", response_model=Conversation)
def create_conversation(
    *,
    db: Session = Depends(deps.get_db),
    conversation_in: ConversationCreate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Create new conversation
    """
    conversation = crud_conversation.create(db, obj_in=conversation_in)
    return conversation

@router.put("/{conversation_id}", response_model=Conversation)
def update_conversation(
    *,
    db: Session = Depends(deps.get_db),
    conversation_id: int,
    conversation_in: ConversationUpdate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Update conversation
    """
    conversation = crud_conversation.get(db, id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation = crud_conversation.update(
        db, db_obj=conversation, obj_in=conversation_in
    )
    return conversation

@router.post("/{conversation_id}/messages", response_model=Message)
def add_message(
    *,
    db: Session = Depends(deps.get_db),
    conversation_id: int,
    message_in: MessageCreate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Add message to conversation
    """
    conversation = crud_conversation.get(db, id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = crud_conversation.add_message(
        db, conversation_id=conversation_id, message_in=message_in
    )
    return message

@router.get("/{conversation_id}/messages", response_model=List[Message])
def list_messages(
    conversation_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    admin: bool = Depends(verify_admin_token)
):
    """
    List messages in conversation
    """
    conversation = crud_conversation.get(db, id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = crud_conversation.get_messages(
        db, conversation_id=conversation_id, skip=skip, limit=limit
    )
    return messages

@router.delete("/{conversation_id}", response_model=Conversation)
def delete_conversation(
    *,
    db: Session = Depends(deps.get_db),
    conversation_id: int,
    admin: bool = Depends(verify_admin_token)
):
    """
    Delete conversation
    """
    conversation = crud_conversation.get(db, id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation = crud_conversation.remove(db, id=conversation_id)
    return conversation 