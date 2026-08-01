import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.ai.providers import ProviderUnavailableException
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

logger = logging.getLogger("main_app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logging
    print("==================================================")
    print(" 🚀 MULTI-PROVIDER AI PLATFORM INITIALIZING      ")
    print("==================================================")
    print(f" • PRIMARY_PROVIDER  : {settings.PRIMARY_PROVIDER.upper()}")
    print(f" • FALLBACK_PROVIDERS: {[p.upper() for p in settings.FALLBACK_PROVIDERS]}")
    print(f" • GROQ_MODELS       : {settings.GROQ_MODELS}")
    print(f" • GEMINI_MODELS     : {settings.GEMINI_MODELS}")
    print(f" • TIMEOUT (SECONDS) : {settings.AI_TIMEOUT_SECONDS}s")
    print(f" • MAX RETRIES       : {settings.AI_MAX_RETRIES}")
    print("==================================================")
    yield


app = FastAPI(
    title="AI Learning Management Platform API",
    description="Backend APIs for AI-Native Learning & Development Platform",
    version="1.0.0",
    lifespan=lifespan
)


@app.exception_handler(ProviderUnavailableException)
async def provider_unavailable_exception_handler(request: Request, exc: ProviderUnavailableException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "success": False,
            "error": exc.message
        }
    )


@app.middleware("http")
async def cors_diagnostic_middleware(request: Request, call_next):
    origin = request.headers.get("origin")
    method = request.method
    path = request.url.path
    
    if origin or method == "OPTIONS":
        logger.info(f"[CORS Audit Request] Method={method} Path={path} Origin={origin}")
    
    response = await call_next(request)
    
    if origin or method == "OPTIONS":
        cors_headers = {k: v for k, v in response.headers.items() if k.lower().startswith("access-control-")}
        logger.info(f"[CORS Audit Response] Method={method} Path={path} Status={response.status_code} Headers={cors_headers}")
        
    return response

# Enable CORS dynamically based on environment config
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
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