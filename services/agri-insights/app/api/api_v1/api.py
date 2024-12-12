from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    users,
    commodities,
    market_data,
    weather,
    alerts,
    watchlists,
    predictions
)

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(commodities.router, prefix="/commodities", tags=["commodities"])
api_router.include_router(market_data.router, prefix="/market-data", tags=["market-data"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(watchlists.router, prefix="/watchlists", tags=["watchlists"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"]) 