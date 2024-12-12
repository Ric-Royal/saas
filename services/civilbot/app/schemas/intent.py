from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime
from app.models.models import LanguageEnum

class TrainingPhraseBase(BaseModel):
    phrase: str
    language: LanguageEnum = LanguageEnum.ENGLISH
    is_active: bool = True
    metadata: Optional[Dict] = None

class TrainingPhraseCreate(TrainingPhraseBase):
    pass

class TrainingPhraseUpdate(TrainingPhraseBase):
    phrase: Optional[str] = None
    language: Optional[LanguageEnum] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict] = None

class TrainingPhrase(TrainingPhraseBase):
    id: int
    intent_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class IntentBase(BaseModel):
    name: str
    description: Optional[str] = None
    training_data: Optional[Dict] = None
    confidence_threshold: int = 70
    is_active: bool = True
    metadata: Optional[Dict] = None

class IntentCreate(IntentBase):
    pass

class IntentUpdate(IntentBase):
    name: Optional[str] = None
    description: Optional[str] = None
    training_data: Optional[Dict] = None
    confidence_threshold: Optional[int] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict] = None

class Intent(IntentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    training_phrases: List[TrainingPhrase] = []

    class Config:
        from_attributes = True 