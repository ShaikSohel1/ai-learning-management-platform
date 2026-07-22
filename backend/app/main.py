from fastapi import FastAPI

app = FastAPI(
    title="AI Learning Management Platform API",
    description="Backend APIs for AI-Native Learning & Development Platform",
    version="1.0.0"
)

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