from datetime import date
from typing import Optional
from pydantic import BaseModel

class PricePredictionBase(BaseModel):
    commodity_id: int
    predicted_price: float
    confidence_score: float
    prediction_date: date
    model_version: str

class PricePredictionCreate(PricePredictionBase):
    pass

class PricePrediction(PricePredictionBase):
    id: int

    class Config:
        orm_mode = True

class HistoricalAnalysisBase(BaseModel):
    commodity_id: int
    date: date
    price: float
    volume: float
    trend_direction: str
    volatility: float
    seasonal_pattern: str

class HistoricalAnalysisCreate(HistoricalAnalysisBase):
    pass

class HistoricalAnalysis(HistoricalAnalysisBase):
    id: int

    class Config:
        orm_mode = True

class PredictionRequest(BaseModel):
    commodity_id: int
    prediction_horizon: int  # days into future
    include_confidence: Optional[bool] = True

class HistoricalAnalysisRequest(BaseModel):
    commodity_id: int
    start_date: date
    end_date: date
    analysis_type: str  # "trend", "seasonality", "volatility", "all" 