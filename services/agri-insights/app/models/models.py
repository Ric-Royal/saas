from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class CommodityType(str, enum.Enum):
    GRAIN = "grain"
    LIVESTOCK = "livestock"
    DAIRY = "dairy"
    FIBER = "fiber"
    ENERGY = "energy"
    METAL = "metal"

class AlertType(str, enum.Enum):
    PRICE = "price"
    WEATHER = "weather"
    MARKET_TREND = "market_trend"
    NEWS = "news"

class AlertCondition(str, enum.Enum):
    ABOVE = "above"
    BELOW = "below"
    EQUALS = "equals"
    PERCENTAGE_CHANGE = "percentage_change"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    preferences = Column(JSON)

    # Relationships
    alerts = relationship("Alert", back_populates="user")
    watchlist = relationship("WatchlistItem", back_populates="user")

class Commodity(Base):
    __tablename__ = "commodities"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(SQLEnum(CommodityType))
    description = Column(String)
    current_price = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)

    # Relationships
    price_history = relationship("PriceHistory", back_populates="commodity")
    watchlist_items = relationship("WatchlistItem", back_populates="commodity")
    alerts = relationship("Alert", back_populates="commodity")
    forecasts = relationship("Forecast", back_populates="commodity")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    timestamp = Column(DateTime, index=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    source = Column(String)

    # Relationships
    commodity = relationship("Commodity", back_populates="price_history")

class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="watchlist")
    commodity = relationship("Commodity", back_populates="watchlist_items")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    alert_type = Column(SQLEnum(AlertType))
    condition = Column(SQLEnum(AlertCondition))
    threshold = Column(Float)
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    notification_channels = Column(JSON)  # e.g., ["email", "sms", "push"]

    # Relationships
    user = relationship("User", back_populates="alerts")
    commodity = relationship("Commodity", back_populates="alerts")

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    forecast_date = Column(DateTime)
    predicted_price = Column(Float)
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    model_version = Column(String)
    features_used = Column(JSON)
    accuracy_metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    commodity = relationship("Commodity", back_populates="forecasts")

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)
    conditions = Column(String)
    source = Column(String)
    raw_data = Column(JSON)

class MarketNews(Base):
    __tablename__ = "market_news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    source = Column(String)
    url = Column(String)
    published_at = Column(DateTime, index=True)
    sentiment_score = Column(Float)
    relevance_score = Column(Float)
    commodities = Column(JSON)  # List of related commodity IDs
    created_at = Column(DateTime, default=datetime.utcnow)

class TradingVolume(Base):
    __tablename__ = "trading_volumes"

    id = Column(Integer, primary_key=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    date = Column(DateTime, index=True)
    volume = Column(Integer)
    value = Column(Float)
    number_of_trades = Column(Integer)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow) 