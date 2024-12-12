from typing import List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Agricultural Market Insights"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str
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
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
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
    REDIS_PASSWORD: Optional[str] = None

    # Celery Configuration
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    @validator("CELERY_BROKER_URL", "CELERY_RESULT_BACKEND", pre=True)
    def assemble_celery_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        password = values.get("REDIS_PASSWORD")
        password_str = f":{password}@" if password else "@"
        return f"redis://{password_str}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/0"

    # Market Data Configuration
    MARKET_DATA_PROVIDERS: List[str] = ["yfinance", "alphavantage"]
    DEFAULT_MARKET_DATA_PROVIDER: str = "yfinance"
    ALPHAVANTAGE_API_KEY: Optional[str] = None
    
    # Weather Data Configuration
    WEATHER_API_KEY: Optional[str] = None
    WEATHER_UPDATE_INTERVAL: int = 3600  # 1 hour
    
    # Cache Configuration
    CACHE_TTL: int = 300  # 5 minutes
    MARKET_DATA_CACHE_TTL: int = 60  # 1 minute
    WEATHER_DATA_CACHE_TTL: int = 1800  # 30 minutes
    
    # Analysis Configuration
    DEFAULT_FORECAST_DAYS: int = 7
    MAX_FORECAST_DAYS: int = 30
    CONFIDENCE_INTERVAL: float = 0.95
    
    # Alert Configuration
    ENABLE_PRICE_ALERTS: bool = True
    ENABLE_WEATHER_ALERTS: bool = True
    ALERT_CHECK_INTERVAL: int = 300  # 5 minutes
    
    # Monitoring Configuration
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 