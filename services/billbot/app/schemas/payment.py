from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class SubscriptionPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    interval: str
    features: Optional[str] = None
    stripe_price_id: str

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlan(SubscriptionPlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    amount: Decimal
    currency: str = "USD"
    payment_method: Optional[str] = None

class PaymentCreate(PaymentBase):
    subscription_plan_id: int

class PaymentUpdate(BaseModel):
    status: str
    stripe_payment_id: Optional[str] = None

class Payment(PaymentBase):
    id: int
    user_id: int
    subscription_plan_id: int
    status: str
    stripe_payment_id: Optional[str]
    stripe_customer_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CreateCheckoutSession(BaseModel):
    plan_id: int
    success_url: str
    cancel_url: str 