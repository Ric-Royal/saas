from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.models import Watchlist, WatchlistItem
from app.schemas.watchlist import WatchlistCreate, WatchlistUpdate

class CRUDWatchlist(CRUDBase[Watchlist, WatchlistCreate, WatchlistUpdate]):
    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Watchlist]:
        return (
            db.query(self.model)
            .filter(Watchlist.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: WatchlistCreate,
        user_id: int
    ) -> Watchlist:
        obj_in_data = obj_in.dict()
        db_obj = Watchlist(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_items(
        self,
        db: Session,
        *,
        watchlist_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[WatchlistItem]:
        return (
            db.query(WatchlistItem)
            .filter(WatchlistItem.watchlist_id == watchlist_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def add_item(
        self,
        db: Session,
        *,
        watchlist_id: int,
        commodity_id: int,
        notes: Optional[str] = None
    ) -> WatchlistItem:
        # Check if item already exists
        existing = (
            db.query(WatchlistItem)
            .filter(
                and_(
                    WatchlistItem.watchlist_id == watchlist_id,
                    WatchlistItem.commodity_id == commodity_id
                )
            )
            .first()
        )
        
        if existing:
            return existing
            
        item = WatchlistItem(
            watchlist_id=watchlist_id,
            commodity_id=commodity_id,
            notes=notes
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def remove_item(
        self,
        db: Session,
        *,
        watchlist_id: int,
        commodity_id: int
    ) -> bool:
        item = (
            db.query(WatchlistItem)
            .filter(
                and_(
                    WatchlistItem.watchlist_id == watchlist_id,
                    WatchlistItem.commodity_id == commodity_id
                )
            )
            .first()
        )
        
        if not item:
            return False
            
        db.delete(item)
        db.commit()
        return True

    def update_item_notes(
        self,
        db: Session,
        *,
        watchlist_id: int,
        commodity_id: int,
        notes: str
    ) -> Optional[WatchlistItem]:
        item = (
            db.query(WatchlistItem)
            .filter(
                and_(
                    WatchlistItem.watchlist_id == watchlist_id,
                    WatchlistItem.commodity_id == commodity_id
                )
            )
            .first()
        )
        
        if not item:
            return None
            
        item.notes = notes
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

watchlist = CRUDWatchlist(Watchlist) 