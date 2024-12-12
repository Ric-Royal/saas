from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, JSON, Enum as SQLEnum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class BillStatus(str, enum.Enum):
    INTRODUCED = "introduced"
    IN_COMMITTEE = "in_committee"
    PASSED_COMMITTEE = "passed_committee"
    FLOOR_VOTE = "floor_vote"
    PASSED = "passed"
    FAILED = "failed"
    VETOED = "vetoed"
    SIGNED = "signed"

class BillType(str, enum.Enum):
    HOUSE_BILL = "house_bill"
    SENATE_BILL = "senate_bill"
    RESOLUTION = "resolution"
    JOINT_RESOLUTION = "joint_resolution"

class Bill(Base):
    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(SQLEnum(BillStatus))
    bill_type = Column(SQLEnum(BillType))
    introduced_date = Column(DateTime)
    last_action_date = Column(DateTime)
    sponsors = Column(JSON)
    full_text_url = Column(String)
    summary = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    versions = relationship("BillVersion", back_populates="bill")
    actions = relationship("BillAction", back_populates="bill")
    votes = relationship("BillVote", back_populates="bill")
    subscriptions = relationship("BillSubscription", back_populates="bill")

class BillVersion(Base):
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bill.id"))
    version_number = Column(Integer)
    version_text = Column(String)
    changes = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bill = relationship("Bill", back_populates="versions")

class BillAction(Base):
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bill.id"))
    action_date = Column(DateTime)
    action_text = Column(String)
    action_type = Column(String)
    committee = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bill = relationship("Bill", back_populates="actions")

class BillVote(Base):
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bill.id"))
    vote_date = Column(DateTime)
    vote_type = Column(String)
    yea_votes = Column(Integer)
    nay_votes = Column(Integer)
    abstain_votes = Column(Integer)
    vote_result = Column(String)
    vote_details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bill = relationship("Bill", back_populates="votes")

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    interval = Column(String, nullable=False)  # monthly, yearly
    features = Column(String)
    stripe_price_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, nullable=False)  # succeeded, pending, failed
    stripe_payment_id = Column(String, unique=True)
    stripe_customer_id = Column(String)
    payment_method = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="payments")
    subscription_plan = relationship("SubscriptionPlan")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    stripe_customer_id = Column(String, unique=True)
    subscription_status = Column(String, default="free")  # free, active, past_due, canceled
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payments = relationship("Payment", back_populates="user")
    subscriptions = relationship("BillSubscription", back_populates="user")

class BillSubscription(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    bill_id = Column(Integer, ForeignKey("bill.id"))
    notify_on_status_change = Column(Boolean, default=True)
    notify_on_vote = Column(Boolean, default=True)
    notify_on_version_change = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    bill = relationship("Bill", back_populates="subscriptions") 