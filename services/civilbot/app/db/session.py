from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from app.core.config import settings
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

@contextmanager
def get_db() -> Session:
    """Get database session with automatic closing."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def get_db_dependency():
    """Dependency for FastAPI endpoints."""
    with get_db() as session:
        yield session

def init_db():
    """Initialize database with required tables."""
    from app.db.base_class import Base
    Base.metadata.create_all(bind=engine)

def close_db_connection():
    """Close database connection pool."""
    engine.dispose() 