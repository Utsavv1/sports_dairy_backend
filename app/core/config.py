from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    OTP_EXPIRE_MINUTES: int = 5
    DATABASE_URL: str = "sqlite+aiosqlite:///./player_app.db"
    
    class Config:
        env_file = ".env"

settings = Settings()

