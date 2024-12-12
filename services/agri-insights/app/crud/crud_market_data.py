from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.crud.base import CRUDBase
from app.models.models import MarketData, PriceTarget
from app.schemas.market_data import (
    MarketDataCreate,
    MarketDataUpdate,
    TimeFrame,
    HistoricalData,
    MarketAnalysis,
    PriceTargetCreate
)

class CRUDMarketData(CRUDBase[MarketData, MarketDataCreate, MarketDataUpdate]):
    def get_historical_data(
        self,
        db: Session,
        *,
        commodity_id: int,
        timeframe: TimeFrame,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[HistoricalData]:
        data = (
            db.query(
                MarketData.date,
                MarketData.price,
                MarketData.volume,
                MarketData.high,
                MarketData.low
            )
            .filter(
                MarketData.commodity_id == commodity_id,
                MarketData.date.between(start_date, end_date)
            )
            .order_by(MarketData.date)
            .all()
        )
        
        if not data:
            return None
            
        return HistoricalData(
            commodity_id=commodity_id,
            timeframe=timeframe,
            data=data
        )

    def get_market_analysis(
        self,
        db: Session,
        *,
        commodity_id: int
    ) -> Optional[MarketAnalysis]:
        # Get latest market data
        latest = (
            db.query(MarketData)
            .filter(MarketData.commodity_id == commodity_id)
            .order_by(desc(MarketData.date))
            .first()
        )
        
        if not latest:
            return None
            
        # Calculate basic statistics
        stats = db.query(
            func.avg(MarketData.price).label('avg_price'),
            func.max(MarketData.price).label('max_price'),
            func.min(MarketData.price).label('min_price'),
            func.avg(MarketData.volume).label('avg_volume')
        ).filter(
            MarketData.commodity_id == commodity_id
        ).first()
        
        return MarketAnalysis(
            commodity_id=commodity_id,
            current_price=latest.price,
            average_price=stats.avg_price,
            highest_price=stats.max_price,
            lowest_price=stats.min_price,
            average_volume=stats.avg_volume,
            price_trend=self._calculate_trend(latest.price, stats.avg_price),
            last_updated=latest.date
        )

    def get_price_targets(
        self,
        db: Session,
        *,
        commodity_id: int
    ) -> List[PriceTarget]:
        return (
            db.query(PriceTarget)
            .filter(PriceTarget.commodity_id == commodity_id)
            .order_by(desc(PriceTarget.created_at))
            .all()
        )

    def create_price_target(
        self,
        db: Session,
        *,
        commodity_id: int,
        target_in: PriceTargetCreate,
        user_id: int
    ) -> PriceTarget:
        target = PriceTarget(
            commodity_id=commodity_id,
            user_id=user_id,
            **target_in.dict()
        )
        db.add(target)
        db.commit()
        db.refresh(target)
        return target

    def _calculate_trend(self, current_price: float, avg_price: float) -> str:
        if current_price > avg_price * 1.05:
            return "upward"
        elif current_price < avg_price * 0.95:
            return "downward"
        return "stable"

market_data = CRUDMarketData(MarketData) 