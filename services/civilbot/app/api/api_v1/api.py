from fastapi import APIRouter
from app.api.api_v1.endpoints import webhooks, users, conversations, intents

api_router = APIRouter()
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(intents.router, prefix="/intents", tags=["intents"]) 