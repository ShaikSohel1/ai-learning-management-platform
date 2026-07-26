from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import Base
from app.database.database import engine
import app.models

from app.routers.auth import router as auth_router
from app.routers.courses import router as course_router
from app.routers.ai import router as ai_router
from app.routers.enrollment import router as enrollment_router
from app.routers.knowledge import router as knowledge_router

from sqlalchemy import text

Base.metadata.create_all(bind=engine)

# Auto-migrate table columns for pre-existing databases
try:
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS progress_percentage INTEGER DEFAULT 0;
            ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS started_at TIMESTAMP;
            ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP;
            ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS certificate_generated BOOLEAN DEFAULT FALSE;
            ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            ALTER TABLE enrollments ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            
            ALTER TABLE certificates ADD COLUMN IF NOT EXISTS certificate_number VARCHAR(100);
            ALTER TABLE certificates ADD COLUMN IF NOT EXISTS issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """))
        conn.commit()
except Exception as e:
    pass

app = FastAPI(
    title="AI Learning Management Platform API",
    description="Backend APIs for AI-Native Learning & Development Platform",
    version="1.0.0"
)

# Enable CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router)
app.include_router(course_router)
app.include_router(ai_router)
app.include_router(enrollment_router)
app.include_router(knowledge_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Learning Management Platform"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }