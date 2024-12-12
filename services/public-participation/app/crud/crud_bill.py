from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Bill
from app.schemas.bill import BillCreate, BillUpdate

class CRUDBill(CRUDBase[Bill, BillCreate, BillUpdate]):
    def get_by_title(self, db: Session, *, title: str) -> Optional[Bill]:
        return db.query(Bill).filter(Bill.title == title).first()

    def get_multi_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Bill]:
        return (
            db.query(Bill)
            .filter(Bill.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_comments(self, db: Session, *, id: int) -> Optional[Bill]:
        return (
            db.query(Bill)
            .filter(Bill.id == id)
            .first()
        )

crud_bill = CRUDBill(Bill) 