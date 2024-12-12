from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud import crud_intent
from app.schemas.intent import (
    Intent,
    IntentCreate,
    IntentUpdate,
    TrainingPhrase,
    TrainingPhraseCreate
)
from app.core.security import verify_admin_token

router = APIRouter()

@router.get("/", response_model=List[Intent])
def list_intents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    admin: bool = Depends(verify_admin_token)
):
    """
    List all intents
    """
    intents = crud_intent.get_multi(db, skip=skip, limit=limit)
    return intents

@router.post("/", response_model=Intent)
def create_intent(
    *,
    db: Session = Depends(deps.get_db),
    intent_in: IntentCreate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Create new intent
    """
    intent = crud_intent.get_by_name(db, name=intent_in.name)
    if intent:
        raise HTTPException(
            status_code=400,
            detail="Intent with this name already exists"
        )
    intent = crud_intent.create(db, obj_in=intent_in)
    return intent

@router.get("/{intent_id}", response_model=Intent)
def get_intent(
    intent_id: int,
    db: Session = Depends(deps.get_db),
    admin: bool = Depends(verify_admin_token)
):
    """
    Get intent by ID
    """
    intent = crud_intent.get(db, id=intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    return intent

@router.put("/{intent_id}", response_model=Intent)
def update_intent(
    *,
    db: Session = Depends(deps.get_db),
    intent_id: int,
    intent_in: IntentUpdate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Update intent
    """
    intent = crud_intent.get(db, id=intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    intent = crud_intent.update(db, db_obj=intent, obj_in=intent_in)
    return intent

@router.delete("/{intent_id}", response_model=Intent)
def delete_intent(
    *,
    db: Session = Depends(deps.get_db),
    intent_id: int,
    admin: bool = Depends(verify_admin_token)
):
    """
    Delete intent
    """
    intent = crud_intent.get(db, id=intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    intent = crud_intent.remove(db, id=intent_id)
    return intent

@router.post("/{intent_id}/training-phrases", response_model=TrainingPhrase)
def add_training_phrase(
    *,
    db: Session = Depends(deps.get_db),
    intent_id: int,
    phrase_in: TrainingPhraseCreate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Add training phrase to intent
    """
    intent = crud_intent.get(db, id=intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    phrase = crud_intent.add_training_phrase(
        db, intent_id=intent_id, phrase_in=phrase_in
    )
    return phrase

@router.get("/{intent_id}/training-phrases", response_model=List[TrainingPhrase])
def list_training_phrases(
    intent_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    admin: bool = Depends(verify_admin_token)
):
    """
    List training phrases for intent
    """
    intent = crud_intent.get(db, id=intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    phrases = crud_intent.get_training_phrases(
        db, intent_id=intent_id, skip=skip, limit=limit
    )
    return phrases 