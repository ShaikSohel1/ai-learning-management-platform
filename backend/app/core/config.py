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
    
    # Multi-Provider AI Configuration
    PRIMARY_PROVIDER: str = os.getenv("PRIMARY_PROVIDER", "groq").lower()
    FALLBACK_PROVIDERS_RAW: str = os.getenv("FALLBACK_PROVIDERS", "gemini")

    # Provider API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # Provider Models Chains
    GROQ_MODELS_RAW: str = os.getenv(
        "GROQ_MODELS",
        "llama-3.3-70b-versatile,deepseek-r1-distill-llama-70b,qwen/qwen3-32b,openai/gpt-oss-120b,llama-3.1-8b-instant"
    )

    GEMINI_MODELS_RAW: str = os.getenv(
        "GEMINI_MODELS",
        "models/gemini-3.6-flash,models/gemini-3.5-flash,models/gemini-flash-latest,models/gemini-3.5-flash-lite,models/gemini-3.1-flash-lite"
    )

    # Retries & Timeouts
    AI_TIMEOUT_SECONDS: float = float(os.getenv("AI_TIMEOUT_SECONDS", os.getenv("AI_REQUEST_TIMEOUT", "30.0")))
    AI_MAX_RETRIES: int = int(os.getenv("AI_MAX_RETRIES", "2"))
    AI_BACKOFF_FACTOR: float = float(os.getenv("AI_BACKOFF_FACTOR", "1.5"))

    # Backward compatibility helpers for internal provider instances
    AI_REQUEST_TIMEOUT: float = AI_TIMEOUT_SECONDS

    @property
    def GROQ_MODELS(self) -> list[str]:
        """Parsed list of Groq model identifiers."""
        return [m.strip() for m in self.GROQ_MODELS_RAW.split(",") if m.strip()]

    @property
    def GEMINI_MODELS(self) -> list[str]:
        """Parsed list of Gemini model identifiers."""
        return [m.strip() for m in self.GEMINI_MODELS_RAW.split(",") if m.strip()]

    @property
    def FALLBACK_PROVIDERS(self) -> list[str]:
        """Parsed list of fallback provider identifiers."""
        return [p.strip().lower() for p in self.FALLBACK_PROVIDERS_RAW.split(",") if p.strip()]


    # Supabase Config
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Resend Email Config
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    RESEND_FROM_EMAIL: str = os.getenv("RESEND_FROM_EMAIL", "AI Learning Platform <onboarding@resend.dev>")


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
