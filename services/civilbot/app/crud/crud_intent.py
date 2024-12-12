from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Intent, TrainingPhrase
from app.schemas.intent import IntentCreate, IntentUpdate, TrainingPhraseCreate

class CRUDIntent(CRUDBase[Intent, IntentCreate, IntentUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Intent]:
        return db.query(Intent).filter(Intent.name == name).first()

    def create(self, db: Session, *, obj_in: IntentCreate) -> Intent:
        db_obj = Intent(
            name=obj_in.name,
            description=obj_in.description,
            training_data=obj_in.training_data,
            confidence_threshold=obj_in.confidence_threshold,
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
        db_obj: Intent,
        obj_in: Union[IntentUpdate, Dict[str, Any]]
    ) -> Intent:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def add_training_phrase(
        self,
        db: Session,
        *,
        intent_id: int,
        phrase_in: TrainingPhraseCreate
    ) -> TrainingPhrase:
        phrase = TrainingPhrase(
            intent_id=intent_id,
            phrase=phrase_in.phrase,
            language=phrase_in.language,
            is_active=phrase_in.is_active,
            metadata=phrase_in.metadata
        )
        db.add(phrase)
        db.commit()
        db.refresh(phrase)
        return phrase

    def get_training_phrases(
        self,
        db: Session,
        *,
        intent_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TrainingPhrase]:
        return (
            db.query(TrainingPhrase)
            .filter(TrainingPhrase.intent_id == intent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

crud_intent = CRUDIntent(Intent) 