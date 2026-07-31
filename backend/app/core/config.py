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
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
    GEMINI_MAX_RETRIES: int = int(os.getenv("GEMINI_MAX_RETRIES", "3"))
    GEMINI_BACKOFF_FACTOR: float = float(os.getenv("GEMINI_BACKOFF_FACTOR", "2.0"))

    # Supabase Config
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # CORS Config
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://ai-learning-management-platform.vercel.app")
    FRONTEND_URLS: str = os.getenv("FRONTEND_URLS", "")

    @property
    def cors_origins(self) -> list[str]:
        defaults = [
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "https://ai-learning-management-platform.vercel.app",
        ]
        custom = []
        for raw_env in (self.FRONTEND_URL, self.FRONTEND_URLS):
            if raw_env:
                for url in raw_env.split(","):
                    cleaned = url.strip().rstrip("/")
                    if cleaned:
                        custom.append(cleaned)
        
        all_origins = []
        for origin in defaults + custom:
            normalized = origin.strip().rstrip("/")
            if normalized and normalized not in all_origins:
                all_origins.append(normalized)
        return all_origins

    @property
    def cors_origin_regex(self) -> str:
        return r"https://.*\.vercel\.app"


settings = Settings()
