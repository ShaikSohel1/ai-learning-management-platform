from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.admin import router as admin_router
from app.routers.agents import router as agents_router
from app.routers.ai import router as ai_router
from app.routers.auth import router as auth_router
from app.routers.courses import router as course_router
from app.routers.enrollment import router as enrollment_router
from app.routers.health import router as health_router
from app.routers.knowledge import router as knowledge_router
from app.routers.notifications import router as notifications_router


app = FastAPI(
    title="AI Learning Management Platform API",
    description="Backend APIs for AI-Native Learning & Development Platform",
    version="1.0.0"
)

# Enable CORS dynamically based on environment config
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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
app.include_router(agents_router)
app.include_router(notifications_router)
app.include_router(health_router)
app.include_router(admin_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Learning Management Platform"
    }