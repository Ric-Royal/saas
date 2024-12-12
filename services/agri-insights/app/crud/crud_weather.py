from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.models import Location, WeatherData, WeatherAlert
from app.schemas.weather import (
    LocationCreate,
    LocationUpdate,
    WeatherSeverity,
    WeatherForecast
)

class CRUDWeather(CRUDBase[WeatherData, LocationCreate, LocationUpdate]):
    def get_locations(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        region: Optional[str] = None
    ) -> List[Location]:
        query = db.query(Location)
        if region:
            query = query.filter(Location.region == region)
        return query.offset(skip).limit(limit).all()

    def get_current_weather(
        self,
        db: Session,
        *,
        location_id: int
    ) -> Optional[WeatherData]:
        return (
            db.query(WeatherData)
            .filter(WeatherData.location_id == location_id)
            .order_by(desc(WeatherData.timestamp))
            .first()
        )

    def get_forecast(
        self,
        db: Session,
        *,
        location_id: int,
        forecast_period: str = "24h"
    ) -> Optional[WeatherForecast]:
        # Convert forecast period to hours
        hours = int(forecast_period.replace("h", ""))
        end_time = datetime.utcnow() + timedelta(hours=hours)
        
        forecasts = (
            db.query(WeatherData)
            .filter(
                WeatherData.location_id == location_id,
                WeatherData.timestamp <= end_time
            )
            .order_by(WeatherData.timestamp)
            .all()
        )
        
        if not forecasts:
            return None
            
        return WeatherForecast(
            location_id=location_id,
            period=forecast_period,
            forecasts=forecasts
        )

    def get_alerts(
        self,
        db: Session,
        *,
        location_id: Optional[int] = None,
        severity: Optional[WeatherSeverity] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[WeatherAlert]:
        query = db.query(WeatherAlert).filter(WeatherAlert.active == True)
        
        if location_id:
            query = query.filter(WeatherAlert.location_id == location_id)
        if severity:
            query = query.filter(WeatherAlert.severity == severity)
            
        return query.offset(skip).limit(limit).all()

    def create_location(
        self,
        db: Session,
        *,
        obj_in: LocationCreate
    ) -> Location:
        location = Location(**obj_in.dict())
        db.add(location)
        db.commit()
        db.refresh(location)
        return location

    def create_alert(
        self,
        db: Session,
        *,
        location_id: int,
        severity: WeatherSeverity,
        message: str
    ) -> WeatherAlert:
        alert = WeatherAlert(
            location_id=location_id,
            severity=severity,
            message=message,
            active=True
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

weather = CRUDWeather(WeatherData) 