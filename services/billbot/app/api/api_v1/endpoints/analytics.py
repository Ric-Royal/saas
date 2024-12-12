from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.services.analytics_service import analytics_service
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/summary", response_model=Dict[str, Any])
def get_summary_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get summary statistics of bills
    """
    return analytics_service.get_summary_stats(db)

@router.get("/trends", response_model=Dict[str, Any])
def get_bill_trends(
    db: Session = Depends(deps.get_db),
    days: int = Query(30, ge=1, le=365),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get bill trends over time
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return analytics_service.get_bill_trends(db, start_date, end_date)

@router.get("/popular-topics", response_model=List[Dict[str, Any]])
def get_popular_topics(
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, ge=1, le=100),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get most popular bill topics
    """
    return analytics_service.get_popular_topics(db, limit)

@router.get("/bill/{bill_id}/analysis", response_model=Dict[str, Any])
def get_bill_analysis(
    bill_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get detailed analysis of a specific bill
    """
    bill = crud.crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return analytics_service.analyze_bill(db, bill)

@router.get("/sponsors/activity", response_model=List[Dict[str, Any]])
def get_sponsor_activity(
    db: Session = Depends(deps.get_db),
    limit: int = Query(20, ge=1, le=100),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get most active bill sponsors
    """
    return analytics_service.get_sponsor_activity(db, limit)

@router.get("/success-rate", response_model=Dict[str, Any])
def get_bill_success_rate(
    db: Session = Depends(deps.get_db),
    days: int = Query(365, ge=1, le=3650),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get bill success rate statistics
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return analytics_service.get_bill_success_rate(db, start_date, end_date)

@router.get("/vote-patterns", response_model=Dict[str, Any])
def get_vote_patterns(
    db: Session = Depends(deps.get_db),
    days: int = Query(30, ge=1, le=365),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get voting patterns analysis
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return analytics_service.get_vote_patterns(db, start_date, end_date) 