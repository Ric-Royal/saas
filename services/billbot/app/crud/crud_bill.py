from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
from app.crud.base import CRUDBase
from app.models.models import Bill, BillVersion, BillAction, BillVote
from app.schemas.bill import BillCreate, BillUpdate, BillVersionCreate, BillActionCreate, BillVoteCreate

class CRUDBill(CRUDBase[Bill, BillCreate, BillUpdate]):
    def get_by_bill_number(self, db: Session, *, bill_number: str) -> Optional[Bill]:
        return db.query(Bill).filter(Bill.bill_number == bill_number).first()

    def get_multi_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> List[Bill]:
        query = db.query(self.model)
        
        if filters:
            if filters.get("status"):
                query = query.filter(self.model.status == filters["status"])
            if filters.get("bill_type"):
                query = query.filter(self.model.bill_type == filters["bill_type"])
            if filters.get("date_from"):
                query = query.filter(self.model.introduced_date >= filters["date_from"])
            if filters.get("date_to"):
                query = query.filter(self.model.introduced_date <= filters["date_to"])
            if filters.get("search_term"):
                search = f"%{filters['search_term']}%"
                query = query.filter(
                    or_(
                        self.model.title.ilike(search),
                        self.model.description.ilike(search),
                        self.model.summary.ilike(search)
                    )
                )
        
        return query.order_by(desc(self.model.introduced_date)).offset(skip).limit(limit).all()

    def create_version(
        self,
        db: Session,
        *,
        obj_in: BillVersionCreate
    ) -> BillVersion:
        db_obj = BillVersion(
            bill_id=obj_in.bill_id,
            version_number=obj_in.version_number,
            version_text=obj_in.version_text,
            changes=obj_in.changes
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_action(
        self,
        db: Session,
        *,
        obj_in: BillActionCreate
    ) -> BillAction:
        db_obj = BillAction(
            bill_id=obj_in.bill_id,
            action_date=obj_in.action_date,
            action_text=obj_in.action_text,
            action_type=obj_in.action_type,
            committee=obj_in.committee
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_vote(
        self,
        db: Session,
        *,
        obj_in: BillVoteCreate
    ) -> BillVote:
        db_obj = BillVote(
            bill_id=obj_in.bill_id,
            vote_date=obj_in.vote_date,
            vote_type=obj_in.vote_type,
            yea_votes=obj_in.yea_votes,
            nay_votes=obj_in.nay_votes,
            abstain_votes=obj_in.abstain_votes,
            vote_result=obj_in.vote_result,
            vote_details=obj_in.vote_details
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_recent_activity(
        self,
        db: Session,
        *,
        days: int = 7
    ) -> List[Bill]:
        date_threshold = datetime.utcnow() - timedelta(days=days)
        return (
            db.query(self.model)
            .filter(
                or_(
                    self.model.updated_at >= date_threshold,
                    self.model.last_action_date >= date_threshold
                )
            )
            .order_by(desc(self.model.updated_at))
            .all()
        )

    def get_by_sponsor(
        self,
        db: Session,
        *,
        sponsor_id: str
    ) -> List[Bill]:
        return (
            db.query(self.model)
            .filter(self.model.sponsors.contains({"id": sponsor_id}))
            .order_by(desc(self.model.introduced_date))
            .all()
        )

crud_bill = CRUDBill(Bill) 