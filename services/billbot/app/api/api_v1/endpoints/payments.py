from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.payment import (
    SubscriptionPlan,
    Payment,
    CreateCheckoutSession
)
from app.services.payment_service import PaymentService
from app.models.models import User

router = APIRouter()

@router.get("/plans", response_model=List[SubscriptionPlan])
def get_subscription_plans(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get all available subscription plans"""
    return db.query(SubscriptionPlan).all()

@router.post("/create-checkout-session")
async def create_checkout_session(
    data: CreateCheckoutSession,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a Stripe checkout session for subscription"""
    session = await PaymentService.create_checkout_session(db, current_user, data)
    return {"session_id": session.id}

@router.get("/subscription-status")
def get_subscription_status(
    current_user: User = Depends(deps.get_current_user)
):
    """Get current user's subscription status"""
    return {
        "status": current_user.subscription_status,
        "current_period_end": current_user.current_period_end
    }

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(deps.get_db),
    stripe_signature: str = Header(None)
):
    """Handle Stripe webhooks"""
    payload = await request.body()
    return await PaymentService.handle_webhook(payload, stripe_signature, db) 