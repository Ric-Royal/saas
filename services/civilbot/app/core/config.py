from typing import List, Union, Optional
from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator
import secrets
from pathlib import Path

class Settings(BaseSettings):
    # Service Info
    PROJECT_NAME: str = "CivilBot"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        secrets.SystemRandom().randrange(360, 480)  # 6-8 hours
    )
    
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
    SQLALCHEMY_DATABASE_URI: Optional[Union[PostgresDsn, str]] = None
    SQLALCHEMY_POOL_SIZE: int = 5
    SQLALCHEMY_MAX_OVERFLOW: int = 10
    SQLALCHEMY_POOL_TIMEOUT: int = 30

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        
        # Ensure all required database values are present
        required = {"POSTGRES_SERVER", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"}
        missing = required - values.keys()
        if missing:
            raise ValueError(f"Missing required database configuration: {missing}")
            
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
    REDIS_PASSWORD: Optional[str] = None
    REDIS_USE_TLS: bool = False

    # Celery Configuration
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    @validator("CELERY_BROKER_URL", "CELERY_RESULT_BACKEND", pre=True)
    def assemble_celery_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
            
        # Build Redis URL for Celery
        password = values.get("REDIS_PASSWORD")
        password_str = f":{password}@" if password else "@"
        tls = "+tls" if values.get("REDIS_USE_TLS") else ""
        return f"redis{tls}://{password_str}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/0"

    # API Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT_LIMIT: int = 100
    RATE_LIMIT_DEFAULT_WINDOW: int = 900  # 15 minutes
    RATE_LIMIT_BY_IP: bool = True

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[Path] = None
    ENABLE_ACCESS_LOG: bool = True

    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Ensure database URL is set
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = self.assemble_db_connection(None, self.dict())
            
        # Set Celery URLs if not provided
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.assemble_celery_connection(None, self.dict())
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.CELERY_BROKER_URL

        # Validate log file path
        if self.LOG_FILE:
            self.LOG_FILE = Path(self.LOG_FILE)
            self.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Create settings instance
settings = Settings() 