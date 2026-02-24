from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-to-a-random-secret-key-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # OTP Settings
    OTP_EXPIRE_MINUTES: int = 5
    OTP_MAX_ATTEMPTS: int = 5  # Max failed attempts before rate limiting
    OTP_SECRET_KEY: str = os.getenv("OTP_SECRET_KEY", "change-this-otp-secret-key")
    
    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "sports_diary")
    
    # Security settings
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "change-this-encryption-key")
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    
    # CORS settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3003,http://localhost:5173").split(",")
    
    class Config:
        env_file = ".env"

settings = Settings()
