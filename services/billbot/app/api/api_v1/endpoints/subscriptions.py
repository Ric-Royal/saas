from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.BillSubscription])
def list_subscriptions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    List user's bill subscriptions
    """
    subscriptions = crud.crud_subscription.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return subscriptions

@router.post("/", response_model=schemas.BillSubscription)
def create_subscription(
    *,
    db: Session = Depends(deps.get_db),
    subscription_in: schemas.BillSubscriptionCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new bill subscription
    """
    # Check if bill exists
    bill = crud.crud_bill.get(db, id=subscription_in.bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    # Check if subscription already exists
    existing_subscription = crud.crud_subscription.get_by_user_and_bill(
        db, user_id=current_user.id, bill_id=subscription_in.bill_id
    )
    if existing_subscription:
        raise HTTPException(
            status_code=400,
            detail="Subscription for this bill already exists"
        )

    subscription = crud.crud_subscription.create_with_user(
        db, obj_in=subscription_in, user_id=current_user.id
    )
    return subscription

@router.get("/{subscription_id}", response_model=schemas.BillSubscription)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get specific subscription
    """
    subscription = crud.crud_subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if subscription.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return subscription

@router.put("/{subscription_id}", response_model=schemas.BillSubscription)
def update_subscription(
    *,
    db: Session = Depends(deps.get_db),
    subscription_id: int,
    subscription_in: schemas.BillSubscriptionUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update subscription settings
    """
    subscription = crud.crud_subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if subscription.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    subscription = crud.crud_subscription.update(
        db, db_obj=subscription, obj_in=subscription_in
    )
    return subscription

@router.delete("/{subscription_id}", response_model=schemas.BillSubscription)
def delete_subscription(
    *,
    db: Session = Depends(deps.get_db),
    subscription_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete subscription
    """
    subscription = crud.crud_subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if subscription.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    subscription = crud.crud_subscription.remove(db, id=subscription_id)
    return subscription 