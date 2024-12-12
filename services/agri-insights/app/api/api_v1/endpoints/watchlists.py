from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Watchlist])
def read_watchlists(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve watchlists."""
    if crud.user.is_superuser(current_user):
        watchlists = crud.watchlist.get_multi(db, skip=skip, limit=limit)
    else:
        watchlists = crud.watchlist.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return watchlists

@router.post("/", response_model=schemas.Watchlist)
def create_watchlist(
    *,
    db: Session = Depends(deps.get_db),
    watchlist_in: schemas.WatchlistCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new watchlist."""
    watchlist = crud.watchlist.create_with_user(
        db=db, obj_in=watchlist_in, user_id=current_user.id
    )
    return watchlist

@router.get("/{watchlist_id}", response_model=schemas.Watchlist)
def read_watchlist(
    *,
    db: Session = Depends(deps.get_db),
    watchlist_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get watchlist by ID."""
    watchlist = crud.watchlist.get(db=db, id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    if not crud.user.is_superuser(current_user) and (watchlist.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return watchlist

@router.put("/{watchlist_id}", response_model=schemas.Watchlist)
def update_watchlist(
    *,
    db: Session = Depends(deps.get_db),
    watchlist_id: int,
    watchlist_in: schemas.WatchlistUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Update a watchlist."""
    watchlist = crud.watchlist.get(db=db, id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    if not crud.user.is_superuser(current_user) and (watchlist.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    watchlist = crud.watchlist.update(
        db=db, db_obj=watchlist, obj_in=watchlist_in
    )
    return watchlist

@router.delete("/{watchlist_id}", response_model=schemas.Watchlist)
def delete_watchlist(
    *,
    db: Session = Depends(deps.get_db),
    watchlist_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Delete a watchlist."""
    watchlist = crud.watchlist.get(db=db, id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    if not crud.user.is_superuser(current_user) and (watchlist.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    watchlist = crud.watchlist.remove(db=db, id=watchlist_id)
    return watchlist

@router.post("/{watchlist_id}/items", response_model=schemas.WatchlistItem)
def add_watchlist_item(
    *,
    db: Session = Depends(deps.get_db),
    watchlist_id: int,
    item_in: schemas.WatchlistItemCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Add item to watchlist."""
    watchlist = crud.watchlist.get(db=db, id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    if not crud.user.is_superuser(current_user) and (watchlist.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.watchlist.add_item(
        db=db, watchlist_id=watchlist_id, item_in=item_in
    )
    return item

@router.delete("/{watchlist_id}/items/{item_id}", response_model=schemas.WatchlistItem)
def remove_watchlist_item(
    *,
    db: Session = Depends(deps.get_db),
    watchlist_id: int,
    item_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Remove item from watchlist."""
    watchlist = crud.watchlist.get(db=db, id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    if not crud.user.is_superuser(current_user) and (watchlist.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.watchlist.remove_item(
        db=db, watchlist_id=watchlist_id, item_id=item_id
    )
    return item

@router.get("/{watchlist_id}/summary", response_model=schemas.WatchlistSummary)
def get_watchlist_summary(
    *,
    db: Session = Depends(deps.get_db),
    watchlist_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get summary of watchlist performance."""
    watchlist = crud.watchlist.get(db=db, id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    if not crud.user.is_superuser(current_user) and (watchlist.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    summary = crud.watchlist.get_summary(db=db, watchlist_id=watchlist_id)
    return summary 