from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "OSINT_System"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./dev_db.db"
    LLM_MODEL_NAME: str = "gemma4-refined:12b"
    # Add other configuration parameters here

    class Config:
        env_file = ".env"

settings = Settings()
