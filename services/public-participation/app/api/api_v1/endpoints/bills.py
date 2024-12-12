from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.services.neo4j_service import add_bill_to_graph
from app.services.redis_service import cache_bill, get_cached_bill

router = APIRouter()

@router.get("/", response_model=List[schemas.Bill])
def read_bills(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = Query(None, description="Filter bills by status"),
) -> Any:
    """
    Retrieve bills.
    """
    if status:
        bills = crud.crud_bill.get_multi_by_status(
            db, status=status, skip=skip, limit=limit
        )
    else:
        bills = crud.crud_bill.get_multi(db, skip=skip, limit=limit)
    return bills

@router.post("/", response_model=schemas.Bill)
def create_bill(
    *,
    db: Session = Depends(deps.get_db),
    bill_in: schemas.BillCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new bill.
    """
    bill = crud.crud_bill.create(db=db, obj_in=bill_in)
    # Add to knowledge graph
    add_bill_to_graph(bill)
    return bill

@router.get("/{id}", response_model=schemas.Bill)
def read_bill(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get bill by ID.
    """
    # Try to get from cache first
    cached_bill = get_cached_bill(id)
    if cached_bill:
        return cached_bill
    
    bill = crud.crud_bill.get(db=db, id=id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Cache the bill for future requests
    cache_bill(bill)
    return bill

@router.put("/{id}", response_model=schemas.Bill)
def update_bill(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    bill_in: schemas.BillUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update bill.
    """
    bill = crud.crud_bill.get(db=db, id=id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    bill = crud.crud_bill.update(db=db, db_obj=bill, obj_in=bill_in)
    return bill

@router.delete("/{id}", response_model=schemas.Bill)
def delete_bill(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete bill.
    """
    bill = crud.crud_bill.get(db=db, id=id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    bill = crud.crud_bill.remove(db=db, id=id)
    return bill 