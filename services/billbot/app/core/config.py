import secrets
from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BillBot"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Configuration
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Union[str, None], values: dict) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Redis Configuration
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = None

    # Bill Tracking Configuration
    BILL_UPDATE_INTERVAL: int = 3600  # 1 hour
    BILL_HISTORY_DAYS: int = 30
    MAX_CONCURRENT_SCRAPES: int = 5

    # NLP Model Configuration
    SPACY_MODEL: str = "en_core_web_sm"
    SENTIMENT_MODEL_PATH: str = "models/sentiment"
    CLASSIFICATION_MODEL_PATH: str = "models/classification"
    MIN_CONFIDENCE_SCORE: float = 0.7

    # Notification Configuration
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    SMTP_HOST: str = None
    SMTP_PORT: int = 587
    SMTP_USER: str = None
    SMTP_PASSWORD: str = None

    # Celery Configuration
    CELERY_BROKER_URL: str = None
    CELERY_RESULT_BACKEND: str = None

    @validator("CELERY_BROKER_URL", "CELERY_RESULT_BACKEND", pre=True)
    def assemble_celery_connection(cls, v: Union[str, None], values: dict) -> str:
        if isinstance(v, str):
            return v
        password = values.get("REDIS_PASSWORD")
        password_str = f":{password}@" if password else "@"
        return f"redis://{password_str}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/0"

    # Stripe settings
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 