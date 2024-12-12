from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base

class LanguageEnum(str, enum.Enum):
    ENGLISH = "en"
    SWAHILI = "sw"
    FRENCH = "fr"

class IntentEnum(str, enum.Enum):
    INQUIRY = "inquiry"
    COMPLAINT = "complaint"
    FEEDBACK = "feedback"
    GENERAL = "general"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    language_preference = Column(Enum(LanguageEnum), default=LanguageEnum.ENGLISH)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    last_interaction = Column(DateTime(timezone=True), nullable=True)
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    notification_enabled = Column(Boolean, default=True)
    daily_updates = Column(Boolean, default=False)
    preferred_topics = Column(JSON, nullable=True)
    quiet_hours_start = Column(Integer, nullable=True)
    quiet_hours_end = Column(Integer, nullable=True)
    user = relationship("User", back_populates="preferences")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    context = Column(JSON, nullable=True)
    intent = Column(Enum(IntentEnum), nullable=True)
    sentiment_score = Column(Integer, nullable=True)
    last_interaction = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text, nullable=False)
    translated_content = Column(JSON, nullable=True)
    is_bot = Column(Boolean, default=False)
    intent = Column(Enum(IntentEnum), nullable=True)
    confidence_score = Column(Integer, nullable=True)
    metadata = Column(JSON, nullable=True)
    conversation = relationship("Conversation", back_populates="messages")

class Intent(Base):
    __tablename__ = "intents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    training_data = Column(JSON, nullable=True)
    confidence_threshold = Column(Integer, default=70)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    training_phrases = relationship("TrainingPhrase", back_populates="intent", cascade="all, delete-orphan")

class TrainingPhrase(Base):
    __tablename__ = "training_phrases"

    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"))
    phrase = Column(Text, nullable=False)
    language = Column(Enum(LanguageEnum), default=LanguageEnum.ENGLISH)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    intent = relationship("Intent", back_populates="training_phrases") 