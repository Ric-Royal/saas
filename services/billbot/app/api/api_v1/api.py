from fastapi import APIRouter
from app.api.api_v1.endpoints import bills, users, auth, subscriptions, analytics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"]) 