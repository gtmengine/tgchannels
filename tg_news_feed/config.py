from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Bot configuration settings loaded from environment variables."""
    
    # Telegram Bot API credentials
    BOT_TOKEN: str
    API_ID: int
    API_HASH: str
    
    # Admin user IDs for special commands
    ADMIN_IDS: List[int]
    
    # Database configuration
    DB_PATH: str = "db.sqlite"
    
    # Feedback form URL
    FEEDBACK_FORM: str
    
    # Parser settings
    PARSER_INTERVAL_MINUTES: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global instance
config = Settings()     
