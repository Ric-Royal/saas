from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/historical/{commodity_id}", response_model=schemas.HistoricalData)
def get_historical_data(
    *,
    db: Session = Depends(deps.get_db),
    commodity_id: int,
    timeframe: schemas.TimeFrame,
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None),
) -> Any:
    """Get historical market data for a commodity."""
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
        
    data = crud.market_data.get_historical_data(
        db,
        commodity_id=commodity_id,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
    )
    if not data:
        raise HTTPException(
            status_code=404,
            detail="No data found for the specified parameters",
        )
    return data

@router.get("/analysis/{commodity_id}", response_model=schemas.MarketAnalysis)
def get_market_analysis(
    *,
    db: Session = Depends(deps.get_db),
    commodity_id: int,
) -> Any:
    """Get market analysis for a commodity."""
    analysis = crud.market_data.get_market_analysis(
        db,
        commodity_id=commodity_id,
    )
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not available for this commodity",
        )
    return analysis

@router.get("/price-targets/{commodity_id}", response_model=List[schemas.PriceTarget])
def get_price_targets(
    *,
    db: Session = Depends(deps.get_db),
    commodity_id: int,
) -> Any:
    """Get price targets for a commodity."""
    targets = crud.market_data.get_price_targets(
        db,
        commodity_id=commodity_id,
    )
    return targets

@router.post("/price-targets/{commodity_id}", response_model=schemas.PriceTarget)
def create_price_target(
    *,
    db: Session = Depends(deps.get_db),
    commodity_id: int,
    target_in: schemas.PriceTarget,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create a new price target for a commodity."""
    target = crud.market_data.create_price_target(
        db,
        commodity_id=commodity_id,
        target_in=target_in,
        user_id=current_user.id,
    )
    return target 