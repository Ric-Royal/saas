from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class TimeFrame(str, Enum):
    MINUTE = "1min"
    FIVE_MINUTES = "5min"
    FIFTEEN_MINUTES = "15min"
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1m"

class MarketDataPoint(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    currency: str = "USD"

    class Config:
        from_attributes = True

class HistoricalData(BaseModel):
    commodity_id: int
    timeframe: TimeFrame
    data: List[MarketDataPoint]
    start_date: datetime
    end_date: datetime
    source: str

class MarketAnalysis(BaseModel):
    commodity_id: int
    timestamp: datetime
    moving_averages: Dict[str, float]  # e.g., "MA20": 45.67
    technical_indicators: Dict[str, float]  # e.g., "RSI": 65.4
    support_levels: List[float]
    resistance_levels: List[float]
    trend: str
    volume_analysis: Dict[str, float]
    
    class Config:
        from_attributes = True

class PriceTarget(BaseModel):
    commodity_id: int
    target_price: float
    confidence: float
    timeframe: str
    analysis_date: datetime
    methodology: str
    supporting_factors: List[str]
    
    class Config:
        from_attributes = True 