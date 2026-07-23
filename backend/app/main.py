from fastapi import FastAPI

from app.database.base import Base
from app.database.database import engine

import app.models
from app.routers.auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Learning Management Platform API",
    description="Backend APIs for AI-Native Learning & Development Platform",
    version="1.0.0"
)
app.include_router(auth_router)

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