from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.crud.base import CRUDBase
from app.models.models import BillSubscription
from app.schemas.subscription import BillSubscriptionCreate, BillSubscriptionUpdate

class CRUDSubscription(CRUDBase[BillSubscription, BillSubscriptionCreate, BillSubscriptionUpdate]):
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[BillSubscription]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_bill(
        self,
        db: Session,
        *,
        bill_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[BillSubscription]:
        return (
            db.query(self.model)
            .filter(self.model.bill_id == bill_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user_and_bill(
        self,
        db: Session,
        *,
        user_id: int,
        bill_id: int
    ) -> Optional[BillSubscription]:
        return (
            db.query(self.model)
            .filter(
                and_(
                    self.model.user_id == user_id,
                    self.model.bill_id == bill_id
                )
            )
            .first()
        )

    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: BillSubscriptionCreate,
        user_id: int
    ) -> BillSubscription:
        db_obj = BillSubscription(
            user_id=user_id,
            bill_id=obj_in.bill_id,
            notify_on_status_change=obj_in.notify_on_status_change,
            notify_on_vote=obj_in.notify_on_vote,
            notify_on_version_change=obj_in.notify_on_version_change
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_subscribers_for_notification(
        self,
        db: Session,
        *,
        bill_id: int,
        notification_type: str
    ) -> List[BillSubscription]:
        filter_condition = {
            "status": self.model.notify_on_status_change,
            "vote": self.model.notify_on_vote,
            "version": self.model.notify_on_version_change
        }.get(notification_type)

        if not filter_condition:
            return []

        return (
            db.query(self.model)
            .filter(
                and_(
                    self.model.bill_id == bill_id,
                    filter_condition == True
                )
            )
            .all()
        )

crud_subscription = CRUDSubscription(BillSubscription) 