from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class PricePrediction(Base):
    __tablename__ = "price_predictions"

    id = Column(Integer, primary_key=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    predicted_price = Column(Float)
    confidence_score = Column(Float)
    prediction_date = Column(Date)
    model_version = Column(String)
    
    commodity = relationship("Commodity", back_populates="predictions")

class HistoricalAnalysis(Base):
    __tablename__ = "historical_analyses"

    id = Column(Integer, primary_key=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    date = Column(Date)
    price = Column(Float)
    volume = Column(Float)
    trend_direction = Column(String)  # "up", "down", "stable"
    volatility = Column(Float)
    seasonal_pattern = Column(String)
    
    commodity = relationship("Commodity", back_populates="historical_analyses") 