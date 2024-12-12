from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Alert])
def read_alerts(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    alert_type: schemas.AlertType = None,
    status: schemas.AlertStatus = None,
) -> Any:
    """Retrieve alerts."""
    alerts = crud.alert.get_multi_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        alert_type=alert_type,
        status=status,
    )
    return alerts

@router.post("/", response_model=schemas.Alert)
def create_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_in: schemas.AlertCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new alert."""
    alert = crud.alert.create_with_user(
        db=db, obj_in=alert_in, user_id=current_user.id
    )
    return alert

@router.get("/{alert_id}", response_model=schemas.Alert)
def read_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get alert by ID."""
    alert = crud.alert.get(db=db, id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return alert

@router.put("/{alert_id}", response_model=schemas.Alert)
def update_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_id: int,
    alert_in: schemas.AlertUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Update an alert."""
    alert = crud.alert.get(db=db, id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    alert = crud.alert.update(db=db, db_obj=alert, obj_in=alert_in)
    return alert

@router.delete("/{alert_id}", response_model=schemas.Alert)
def delete_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Delete an alert."""
    alert = crud.alert.get(db=db, id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    alert = crud.alert.remove(db=db, id=alert_id)
    return alert

@router.get("/logs/{alert_id}", response_model=List[schemas.AlertLog])
def read_alert_logs(
    *,
    db: Session = Depends(deps.get_db),
    alert_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get alert logs."""
    alert = crud.alert.get(db=db, id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    logs = crud.alert.get_logs(
        db=db, alert_id=alert_id, skip=skip, limit=limit
    )
    return logs 