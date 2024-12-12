from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from app.api import deps
from app.schemas.prediction import (
    PredictionRequest,
    HistoricalAnalysisRequest,
    PricePrediction,
    HistoricalAnalysis
)
from app.services.ml_service import ml_service
from app.crud.crud_market_data import crud_market_data

router = APIRouter()

@router.post("/predict/", response_model=List[PricePrediction])
def predict_prices(
    request: PredictionRequest,
    db: Session = Depends(deps.get_db)
):
    """
    Get price predictions for a commodity
    """
    # Get historical data for the commodity
    historical_data = crud_market_data.get_commodity_history(
        db=db,
        commodity_id=request.commodity_id,
        days=60  # Get last 60 days for prediction
    )
    
    if not historical_data:
        raise HTTPException(
            status_code=404,
            detail="No historical data found for this commodity"
        )
    
    # Convert to pandas DataFrame
    df = pd.DataFrame([h.__dict__ for h in historical_data])
    
    # Get predictions
    predictions = ml_service.predict_price(
        historical_data=df,
        horizon=request.prediction_horizon
    )
    
    # Format response
    result = []
    for i, (pred, conf) in enumerate(zip(
        predictions["predictions"],
        predictions["confidence_scores"]
    )):
        result.append(PricePrediction(
            commodity_id=request.commodity_id,
            predicted_price=pred,
            confidence_score=conf if request.include_confidence else None,
            prediction_date=df['date'].iloc[-1] + pd.Timedelta(days=i+1),
            model_version=predictions["model_version"]
        ))
    
    return result

@router.post("/analyze/", response_model=dict)
def analyze_historical_data(
    request: HistoricalAnalysisRequest,
    db: Session = Depends(deps.get_db)
):
    """
    Analyze historical data for a commodity
    """
    # Get historical data
    historical_data = crud_market_data.get_commodity_history_range(
        db=db,
        commodity_id=request.commodity_id,
        start_date=request.start_date,
        end_date=request.end_date
    )
    
    if not historical_data:
        raise HTTPException(
            status_code=404,
            detail="No historical data found for this period"
        )
    
    # Convert to pandas DataFrame
    df = pd.DataFrame([h.__dict__ for h in historical_data])
    
    # Perform analysis
    analysis_results = ml_service.analyze_historical_data(
        data=df,
        analysis_type=request.analysis_type
    )
    
    return analysis_results

@router.post("/train/")
def train_model(db: Session = Depends(deps.get_db)):
    """
    Train/retrain the ML model with latest data
    """
    # Get all historical data for training
    historical_data = crud_market_data.get_all_market_data(db)
    
    if not historical_data:
        raise HTTPException(
            status_code=404,
            detail="No historical data available for training"
        )
    
    # Convert to pandas DataFrame
    df = pd.DataFrame([h.__dict__ for h in historical_data])
    
    # Train the model
    ml_service.train_model(df)
    
    return {"message": "Model trained successfully"} 