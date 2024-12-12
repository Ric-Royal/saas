from typing import Optional, Dict, List
from pydantic import BaseModel, constr
from datetime import datetime
from app.models.models import LanguageEnum

class UserPreferenceBase(BaseModel):
    notification_enabled: bool = True
    daily_updates: bool = False
    preferred_topics: Optional[List[str]] = None
    quiet_hours_start: Optional[int] = None
    quiet_hours_end: Optional[int] = None

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceUpdate(UserPreferenceBase):
    pass

class UserBase(BaseModel):
    phone_number: constr(regex=r'^\+[1-9]\d{1,14}$')
    language_preference: LanguageEnum = LanguageEnum.ENGLISH
    is_active: bool = True
    metadata: Optional[Dict] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    phone_number: Optional[constr(regex=r'^\+[1-9]\d{1,14}$')] = None
    language_preference: Optional[LanguageEnum] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict] = None

class UserPreference(UserPreferenceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    last_interaction: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    preferences: Optional[UserPreference] = None

    class Config:
        from_attributes = True 