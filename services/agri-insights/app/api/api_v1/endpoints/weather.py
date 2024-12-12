from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/locations", response_model=List[schemas.Location])
def get_locations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    region: str = None,
) -> Any:
    """Get list of monitored locations."""
    locations = crud.weather.get_locations(
        db, skip=skip, limit=limit, region=region
    )
    return locations

@router.get("/current/{location_id}", response_model=schemas.WeatherData)
def get_current_weather(
    *,
    db: Session = Depends(deps.get_db),
    location_id: int,
) -> Any:
    """Get current weather data for a location."""
    weather = crud.weather.get_current_weather(db, location_id=location_id)
    if not weather:
        raise HTTPException(
            status_code=404,
            detail="Weather data not available for this location",
        )
    return weather

@router.get("/forecast/{location_id}", response_model=schemas.WeatherForecast)
def get_weather_forecast(
    *,
    db: Session = Depends(deps.get_db),
    location_id: int,
    forecast_period: str = "24h",
) -> Any:
    """Get weather forecast for a location."""
    forecast = crud.weather.get_forecast(
        db,
        location_id=location_id,
        forecast_period=forecast_period,
    )
    if not forecast:
        raise HTTPException(
            status_code=404,
            detail="Forecast not available for this location",
        )
    return forecast

@router.get("/alerts", response_model=List[schemas.WeatherAlert])
def get_weather_alerts(
    *,
    db: Session = Depends(deps.get_db),
    location_id: int = None,
    severity: schemas.WeatherSeverity = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get active weather alerts."""
    alerts = crud.weather.get_alerts(
        db,
        location_id=location_id,
        severity=severity,
        skip=skip,
        limit=limit,
    )
    return alerts

@router.post("/locations", response_model=schemas.Location)
def create_location(
    *,
    db: Session = Depends(deps.get_db),
    location_in: schemas.Location,
    current_user: models.User = Depends(deps.get_current_superuser),
) -> Any:
    """Add a new location for weather monitoring."""
    location = crud.weather.create_location(db, obj_in=location_in)
    return location 