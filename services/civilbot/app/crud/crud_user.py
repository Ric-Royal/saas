from typing import Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import User, UserPreference
from app.schemas.user import UserCreate, UserUpdate, UserPreferenceUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_phone(self, db: Session, *, phone_number: str) -> Optional[User]:
        return db.query(User).filter(User.phone_number == phone_number).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            phone_number=obj_in.phone_number,
            language_preference=obj_in.language_preference,
            is_active=obj_in.is_active,
            metadata=obj_in.metadata
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def update_preferences(
        self,
        db: Session,
        *,
        db_obj: User,
        preferences_in: UserPreferenceUpdate
    ) -> User:
        if not db_obj.preferences:
            preferences = UserPreference(
                user_id=db_obj.id,
                **preferences_in.dict()
            )
            db.add(preferences)
        else:
            for key, value in preferences_in.dict(exclude_unset=True).items():
                setattr(db_obj.preferences, key, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_active(self, user: User) -> bool:
        return user.is_active

crud_user = CRUDUser(User) 