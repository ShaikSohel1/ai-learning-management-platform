import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Learning Management Platform"
    VERSION: str = "1.0.0"
    
    # Secret keys & auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-later")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://shaiksohel@localhost/ai_learning_db")
    
    # Gemini AI Config
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    GEMINI_MAX_RETRIES: int = int(os.getenv("GEMINI_MAX_RETRIES", "3"))
    GEMINI_BACKOFF_FACTOR: float = float(os.getenv("GEMINI_BACKOFF_FACTOR", "2.0"))

settings = Settings()
