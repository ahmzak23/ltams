from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ticket Booking System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenTelemetry
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://otel-collector:4317"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 