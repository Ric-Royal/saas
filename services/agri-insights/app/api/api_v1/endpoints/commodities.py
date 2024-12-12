from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Commodity])
def read_commodities(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    commodity_type: schemas.CommodityType = None,
) -> Any:
    """Retrieve commodities."""
    commodities = crud.commodity.get_multi(
        db, skip=skip, limit=limit, commodity_type=commodity_type
    )
    return commodities

@router.post("/", response_model=schemas.Commodity)
def create_commodity(
    *,
    db: Session = Depends(deps.get_db),
    commodity_in: schemas.CommodityCreate,
    current_user: models.User = Depends(deps.get_current_superuser),
) -> Any:
    """Create new commodity."""
    commodity = crud.commodity.create(db, obj_in=commodity_in)
    return commodity

@router.get("/{commodity_id}", response_model=schemas.CommodityWithPrices)
def read_commodity(
    *,
    db: Session = Depends(deps.get_db),
    commodity_id: int,
) -> Any:
    """Get commodity by ID."""
    commodity = crud.commodity.get(db, id=commodity_id)
    if not commodity:
        raise HTTPException(
            status_code=404,
            detail="Commodity not found",
        )
    return commodity

@router.put("/{commodity_id}", response_model=schemas.Commodity)
def update_commodity(
    *,
    db: Session = Depends(deps.get_db),
    commodity_id: int,
    commodity_in: schemas.CommodityUpdate,
    current_user: models.User = Depends(deps.get_current_superuser),
) -> Any:
    """Update a commodity."""
    commodity = crud.commodity.get(db, id=commodity_id)
    if not commodity:
        raise HTTPException(
            status_code=404,
            detail="Commodity not found",
        )
    commodity = crud.commodity.update(
        db, db_obj=commodity, obj_in=commodity_in
    )
    return commodity

@router.get("/{commodity_id}/prices", response_model=List[schemas.CommodityPrice])
def read_commodity_prices(
    *,
    db: Session = Depends(deps.get_db),
    commodity_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get price history for a commodity."""
    commodity = crud.commodity.get(db, id=commodity_id)
    if not commodity:
        raise HTTPException(
            status_code=404,
            detail="Commodity not found",
        )
    prices = crud.commodity.get_prices(
        db, commodity_id=commodity_id, skip=skip, limit=limit
    )
    return prices 