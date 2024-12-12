from typing import Optional, List, Dict, Union
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class AlertType(str, Enum):
    PRICE = "price"
    WEATHER = "weather"
    MARKET_ANALYSIS = "market_analysis"
    NEWS = "news"

class AlertPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(str, Enum):
    ACTIVE = "active"
    TRIGGERED = "triggered"
    DISMISSED = "dismissed"
    EXPIRED = "expired"

class AlertCondition(BaseModel):
    field: str  # e.g., "price", "temperature", "rsi"
    operator: str  # e.g., ">", "<", "=", "between"
    value: Union[float, List[float]]  # single value or range
    time_window: Optional[str] = None  # e.g., "1h", "24h"

class AlertBase(BaseModel):
    user_id: int
    type: AlertType
    commodity_id: Optional[int] = None
    location_id: Optional[int] = None
    priority: AlertPriority = AlertPriority.MEDIUM
    conditions: List[AlertCondition]
    notification_channels: List[str]  # e.g., ["email", "sms", "push"]
    expiration: Optional[datetime] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    priority: Optional[AlertPriority] = None
    conditions: Optional[List[AlertCondition]] = None
    notification_channels: Optional[List[str]] = None
    expiration: Optional[datetime] = None
    status: Optional[AlertStatus] = None

class Alert(AlertBase):
    id: int
    status: AlertStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0
    
    class Config:
        from_attributes = True

class AlertLog(BaseModel):
    alert_id: int
    timestamp: datetime
    event_type: str  # e.g., "triggered", "notification_sent", "status_changed"
    details: Dict
    
    class Config:
        from_attributes = True 