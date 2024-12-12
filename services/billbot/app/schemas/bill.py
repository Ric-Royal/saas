from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel
from app.models.models import BillStatus, BillType

class BillVersionBase(BaseModel):
    version_number: int
    version_text: str
    changes: Optional[Dict] = None

class BillVersionCreate(BillVersionBase):
    bill_id: int

class BillVersion(BillVersionBase):
    id: int
    bill_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BillActionBase(BaseModel):
    action_date: datetime
    action_text: str
    action_type: str
    committee: Optional[str] = None

class BillActionCreate(BillActionBase):
    bill_id: int

class BillAction(BillActionBase):
    id: int
    bill_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BillVoteBase(BaseModel):
    vote_date: datetime
    vote_type: str
    yea_votes: int
    nay_votes: int
    abstain_votes: int
    vote_result: str
    vote_details: Optional[Dict] = None

class BillVoteCreate(BillVoteBase):
    bill_id: int

class BillVote(BillVoteBase):
    id: int
    bill_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BillBase(BaseModel):
    bill_number: str
    title: str
    description: str
    status: BillStatus
    bill_type: BillType
    introduced_date: datetime
    last_action_date: Optional[datetime] = None
    sponsors: Optional[Dict] = None
    full_text_url: Optional[str] = None
    summary: Optional[str] = None
    metadata: Optional[Dict] = None

class BillCreate(BillBase):
    pass

class BillUpdate(BillBase):
    bill_number: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BillStatus] = None
    bill_type: Optional[BillType] = None
    introduced_date: Optional[datetime] = None

class Bill(BillBase):
    id: int
    created_at: datetime
    updated_at: datetime
    versions: List[BillVersion] = []
    actions: List[BillAction] = []
    votes: List[BillVote] = []

    class Config:
        from_attributes = True 