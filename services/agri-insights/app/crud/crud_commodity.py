from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.models import Commodity, CommodityPrice
from app.schemas.commodity import CommodityCreate, CommodityUpdate
from app.schemas.market_data import CommodityType

class CRUDCommodity(CRUDBase[Commodity, CommodityCreate, CommodityUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        commodity_type: Optional[CommodityType] = None
    ) -> List[Commodity]:
        query = db.query(self.model)
        if commodity_type:
            query = query.filter(self.model.type == commodity_type)
        return query.offset(skip).limit(limit).all()

    def get_prices(
        self,
        db: Session,
        *,
        commodity_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[CommodityPrice]:
        return (
            db.query(CommodityPrice)
            .filter(CommodityPrice.commodity_id == commodity_id)
            .order_by(desc(CommodityPrice.date))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name(self, db: Session, *, name: str) -> Optional[Commodity]:
        return db.query(self.model).filter(self.model.name == name).first()

    def create_with_price(
        self,
        db: Session,
        *,
        obj_in: CommodityCreate,
        price: float
    ) -> Commodity:
        commodity = self.create(db, obj_in=obj_in)
        price_obj = CommodityPrice(
            commodity_id=commodity.id,
            price=price
        )
        db.add(price_obj)
        db.commit()
        db.refresh(commodity)
        return commodity

commodity = CRUDCommodity(Commodity) 