from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from .comment import Comment

class BillBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "draft"
    pdf_url: Optional[str] = None

class BillCreate(BillBase):
    pass

class BillUpdate(BillBase):
    pass

class Bill(BillBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[Comment] = []

    class Config:
        from_attributes = True 