from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.services.bill_service import bill_service
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[schemas.Bill])
def list_bills(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[models.BillStatus] = None,
    bill_type: Optional[models.BillType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve bills with optional filters
    """
    filters = {
        "status": status,
        "bill_type": bill_type,
        "start_date": start_date,
        "end_date": end_date
    }
    bills = crud.crud_bill.get_multi_with_filters(
        db, skip=skip, limit=limit, filters=filters
    )
    return bills

@router.get("/{bill_id}", response_model=schemas.Bill)
def get_bill(
    bill_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get specific bill by ID
    """
    bill = crud.crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

@router.get("/{bill_id}/versions", response_model=List[schemas.BillVersion])
def get_bill_versions(
    bill_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get versions of a specific bill
    """
    bill = crud.crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return crud.crud_bill.get_versions(db, bill_id=bill_id, skip=skip, limit=limit)

@router.get("/{bill_id}/actions", response_model=List[schemas.BillAction])
def get_bill_actions(
    bill_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get actions of a specific bill
    """
    bill = crud.crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return crud.crud_bill.get_actions(db, bill_id=bill_id, skip=skip, limit=limit)

@router.get("/{bill_id}/votes", response_model=List[schemas.BillVote])
def get_bill_votes(
    bill_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get votes of a specific bill
    """
    bill = crud.crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return crud.crud_bill.get_votes(db, bill_id=bill_id, skip=skip, limit=limit)

@router.post("/{bill_id}/refresh", response_model=schemas.Bill)
def refresh_bill(
    bill_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Manually trigger a refresh of bill data (admin only)
    """
    bill = crud.crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    updated_bill = bill_service.refresh_bill(db, bill)
    return updated_bill

@router.get("/search", response_model=List[schemas.Bill])
def search_bills(
    query: str = Query(..., min_length=3),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Search bills by title, description, or content
    """
    bills = crud.crud_bill.search(
        db, query=query, skip=skip, limit=limit
    )
    return bills 