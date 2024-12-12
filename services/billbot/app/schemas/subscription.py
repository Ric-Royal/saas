from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BillSubscriptionBase(BaseModel):
    notify_on_status_change: bool = True
    notify_on_vote: bool = True
    notify_on_version_change: bool = True

class BillSubscriptionCreate(BillSubscriptionBase):
    bill_id: int

class BillSubscriptionUpdate(BillSubscriptionBase):
    notify_on_status_change: Optional[bool] = None
    notify_on_vote: Optional[bool] = None
    notify_on_version_change: Optional[bool] = None

class BillSubscription(BillSubscriptionBase):
    id: int
    user_id: int
    bill_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 