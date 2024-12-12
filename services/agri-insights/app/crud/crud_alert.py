from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.models import Alert, AlertLog
from app.schemas.alert import AlertCreate, AlertUpdate, AlertType, AlertStatus

class CRUDAlert(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        alert_type: Optional[AlertType] = None,
        status: Optional[AlertStatus] = None
    ) -> List[Alert]:
        query = db.query(self.model).filter(Alert.user_id == user_id)
        
        if alert_type:
            query = query.filter(Alert.type == alert_type)
        if status:
            query = query.filter(Alert.status == status)
            
        return query.offset(skip).limit(limit).all()

    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: AlertCreate,
        user_id: int
    ) -> Alert:
        obj_in_data = obj_in.dict()
        db_obj = Alert(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_logs(
        self,
        db: Session,
        *,
        alert_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AlertLog]:
        return (
            db.query(AlertLog)
            .filter(AlertLog.alert_id == alert_id)
            .order_by(desc(AlertLog.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_log(
        self,
        db: Session,
        *,
        alert_id: int,
        message: str,
        status: AlertStatus
    ) -> AlertLog:
        log = AlertLog(
            alert_id=alert_id,
            message=message,
            status=status,
            created_at=datetime.utcnow()
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def update_status(
        self,
        db: Session,
        *,
        alert_id: int,
        status: AlertStatus,
        message: Optional[str] = None
    ) -> Alert:
        alert = self.get(db, id=alert_id)
        if not alert:
            return None
            
        alert.status = status
        alert.last_updated = datetime.utcnow()
        
        if message:
            self.create_log(db, alert_id=alert_id, message=message, status=status)
            
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

alert = CRUDAlert(Alert) 