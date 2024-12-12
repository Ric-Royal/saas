from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .user import User

class CommentBase(BaseModel):
    text: str
    bill_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[User] = None

    class Config:
        from_attributes = True 