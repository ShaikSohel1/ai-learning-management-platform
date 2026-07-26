from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import Base
from app.database.database import engine
import app.models

from app.routers.auth import router as auth_router
from app.routers.courses import router as course_router

Base.metadata.create_all(bind=engine)

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