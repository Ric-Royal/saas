from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel

class WatchlistItemBase(BaseModel):
    commodity_id: int
    notes: Optional[str] = None
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    metadata: Optional[Dict] = None

class WatchlistItemCreate(WatchlistItemBase):
    pass

class WatchlistItemUpdate(WatchlistItemBase):
    commodity_id: Optional[int] = None

class WatchlistItem(WatchlistItemBase):
    id: int
    watchlist_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_price: Optional[float] = None
    last_update: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WatchlistBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    metadata: Optional[Dict] = None

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistUpdate(WatchlistBase):
    name: Optional[str] = None

class Watchlist(WatchlistBase):
    id: int
    user_id: int
    items: List[WatchlistItem] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WatchlistSummary(BaseModel):
    watchlist_id: int
    total_items: int
    price_changes: Dict[int, float]  # commodity_id: price_change
    performance_metrics: Dict[str, float]
    last_update: datetime
    
    class Config:
        from_attributes = True 