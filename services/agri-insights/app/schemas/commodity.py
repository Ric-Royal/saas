from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class CommodityType(str, Enum):
    GRAIN = "grain"
    LIVESTOCK = "livestock"
    DAIRY = "dairy"
    FIBER = "fiber"
    OILSEED = "oilseed"
    SPECIALTY = "specialty"

class CommodityBase(BaseModel):
    name: str
    symbol: str
    type: CommodityType
    description: Optional[str] = None
    unit: str
    is_active: bool = True
    metadata: Optional[Dict] = None

class CommodityCreate(CommodityBase):
    pass

class CommodityUpdate(CommodityBase):
    name: Optional[str] = None
    symbol: Optional[str] = None
    type: Optional[CommodityType] = None
    unit: Optional[str] = None

class Commodity(CommodityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommodityPrice(BaseModel):
    commodity_id: int
    price: float
    currency: str = "USD"
    timestamp: datetime
    source: str
    volume: Optional[float] = None
    
    class Config:
        from_attributes = True

class CommodityWithPrices(Commodity):
    prices: List[CommodityPrice] = [] 