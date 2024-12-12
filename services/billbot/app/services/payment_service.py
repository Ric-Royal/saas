import stripe
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud.crud_user import crud_user
from app.models.models import User, SubscriptionPlan
from app.schemas.payment import CreateCheckoutSession

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    @staticmethod
    async def create_customer(user: User, email: str) -> str:
        if user.stripe_customer_id:
            return user.stripe_customer_id
            
        customer = stripe.Customer.create(
            email=email,
            metadata={"user_id": user.id}
        )
        return customer.id

    @staticmethod
    async def create_checkout_session(
        db: Session,
        user: User,
        data: CreateCheckoutSession
    ):
        # Get subscription plan
        plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == data.plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Subscription plan not found")

        # Ensure user has Stripe customer ID
        if not user.stripe_customer_id:
            customer_id = await PaymentService.create_customer(user, user.email)
            user.stripe_customer_id = customer_id
            db.commit()
        
        # Create checkout session
        try:
            session = stripe.checkout.Session.create(
                customer=user.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=data.success_url,
                cancel_url=data.cancel_url,
                metadata={
                    'user_id': user.id,
                    'plan_id': plan.id
                }
            )
            return session
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def handle_webhook(payload: dict, sig_header: str, db: Session):
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")

        event_object = event.data.object

        if event.type == 'checkout.session.completed':
            # Handle successful checkout
            user_id = event_object.metadata.get('user_id')
            user = crud_user.get(db, id=user_id)
            if user:
                user.subscription_status = 'active'
                db.commit()

        elif event.type == 'invoice.payment_succeeded':
            # Handle successful subscription payment
            customer_id = event_object.customer
            user = crud_user.get_by_stripe_customer_id(db, customer_id)
            if user:
                user.subscription_status = 'active'
                user.current_period_end = event_object.lines.data[0].period.end
                db.commit()

        elif event.type == 'invoice.payment_failed':
            # Handle failed payment
            customer_id = event_object.customer
            user = crud_user.get_by_stripe_customer_id(db, customer_id)
            if user:
                user.subscription_status = 'past_due'
                db.commit()

        elif event.type == 'customer.subscription.deleted':
            # Handle subscription cancellation
            customer_id = event_object.customer
            user = crud_user.get_by_stripe_customer_id(db, customer_id)
            if user:
                user.subscription_status = 'canceled'
                db.commit()

        return {"status": "success"} 