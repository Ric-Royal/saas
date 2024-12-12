from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class WeatherType(str, Enum):
    SUNNY = "sunny"
    PARTLY_CLOUDY = "partly_cloudy"
    CLOUDY = "cloudy"
    RAIN = "rain"
    THUNDERSTORM = "thunderstorm"
    SNOW = "snow"
    FOG = "fog"

class WeatherSeverity(str, Enum):
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXTREME = "extreme"

class WeatherData(BaseModel):
    location_id: int
    timestamp: datetime
    temperature: float
    humidity: float
    precipitation: float
    wind_speed: float
    wind_direction: float
    pressure: float
    weather_type: WeatherType
    severity: WeatherSeverity = WeatherSeverity.NONE
    alerts: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class WeatherForecast(BaseModel):
    location_id: int
    forecast_time: datetime
    forecast_period: str  # e.g., "24h", "7d"
    hourly_data: List[WeatherData]
    daily_summary: Dict[str, float]  # e.g., {"avg_temp": 25.5, "total_precip": 10.2}
    confidence: float
    source: str
    
    class Config:
        from_attributes = True

class WeatherAlert(BaseModel):
    location_id: int
    alert_type: str
    severity: WeatherSeverity
    start_time: datetime
    end_time: datetime
    description: str
    recommendations: List[str]
    affected_commodities: List[int]  # List of commodity IDs
    
    class Config:
        from_attributes = True

class Location(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    region: str
    country: str
    timezone: str
    active_commodities: List[int]  # List of commodity IDs
    
    class Config:
        from_attributes = True 