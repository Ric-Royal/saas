from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_bill
from app.models.models import User
from app.schemas.bill import Bill, BillCreate, BillUpdate

router = APIRouter()

@router.get("/bills", response_model=List[Bill])
def get_bills(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all bills. Only accessible by superusers.
    """
    bills = crud_bill.get_multi(db, skip=skip, limit=limit)
    return bills

@router.post("/bills", response_model=Bill)
def create_bill(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
    bill_in: BillCreate,
):
    """
    Create new bill. Only accessible by superusers.
    """
    bill = crud_bill.create(db, obj_in=bill_in)
    return bill

@router.put("/bills/{bill_id}", response_model=Bill)
def update_bill(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
    bill_id: int,
    bill_in: BillUpdate,
):
    """
    Update bill. Only accessible by superusers.
    """
    bill = crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found",
        )
    bill = crud_bill.update(db, db_obj=bill, obj_in=bill_in)
    return bill

@router.delete("/bills/{bill_id}")
def delete_bill(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
    bill_id: int,
):
    """
    Delete bill. Only accessible by superusers.
    """
    bill = crud_bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found",
        )
    crud_bill.remove(db, id=bill_id)
    return {"status": "success"} 