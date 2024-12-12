from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Comment, User
from app.schemas.comment import CommentCreate, CommentUpdate

class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: CommentCreate, user_id: int
    ) -> Comment:
        db_obj = Comment(
            text=obj_in.text,
            bill_id=obj_in.bill_id,
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_bill(
        self, db: Session, *, bill_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return (
            db.query(Comment)
            .filter(Comment.bill_id == bill_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return (
            db.query(Comment)
            .filter(Comment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

crud_comment = CRUDComment(Comment) 