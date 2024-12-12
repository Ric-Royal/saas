from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, between
from datetime import datetime
from app.crud.base import CRUDBase
from app.models.models import Conversation, Message
from app.schemas.conversation import ConversationCreate, ConversationUpdate, MessageCreate

class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    def get_multi_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> List[Conversation]:
        query = db.query(self.model)
        
        if filters:
            if filters.get("user_id"):
                query = query.filter(self.model.user_id == filters["user_id"])
            if filters.get("is_active") is not None:
                query = query.filter(self.model.is_active == filters["is_active"])
            if filters.get("start_date") and filters.get("end_date"):
                query = query.filter(between(
                    self.model.created_at,
                    filters["start_date"],
                    filters["end_date"]
                ))
        
        return query.offset(skip).limit(limit).all()

    def get_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Conversation]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_by_user(
        self,
        db: Session,
        *,
        user_id: int
    ) -> Optional[Conversation]:
        return (
            db.query(self.model)
            .filter(
                and_(
                    self.model.user_id == user_id,
                    self.model.is_active == True
                )
            )
            .first()
        )

    def add_message(
        self,
        db: Session,
        *,
        conversation_id: int,
        message_in: MessageCreate
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            content=message_in.content,
            is_bot=message_in.is_bot,
            intent=message_in.intent,
            confidence_score=message_in.confidence_score,
            metadata=message_in.metadata
        )
        db.add(message)
        
        # Update conversation last_interaction
        conversation = self.get(db, id=conversation_id)
        conversation.last_interaction = datetime.utcnow()
        db.add(conversation)
        
        db.commit()
        db.refresh(message)
        return message

    def get_messages(
        self,
        db: Session,
        *,
        conversation_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Message]:
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

crud_conversation = CRUDConversation(Conversation) 