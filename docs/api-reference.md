# Comprehensive API Reference

This document provides complete documentation for all REST API endpoints available in the **AI Learning Management Platform**.

---

## 🔑 Authentication Endpoints (`/auth`)

### `POST /auth/register`
- **Summary**: Register a new user account.
- **Auth**: None
- **Request Body**:
  ```json
  {
    "email": "employee@company.com",
    "password": "SecurePassword123!",
    "full_name": "Jane Doe",
    "role": "student"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "id": "1e7a6890-278b-416e-96c0-4eb28aea8e58",
    "email": "employee@company.com",
    "full_name": "Jane Doe",
    "role": "student",
    "is_active": true
  }
  ```

### `POST /auth/login`
- **Summary**: Authenticate user and issue JWT token.
- **Auth**: None (OAuth2 Form / JSON)
- **Response** (`200 OK`):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": "1e7a6890-278b-416e-96c0-4eb28aea8e58",
      "email": "employee@company.com",
      "full_name": "Jane Doe",
      "role": "student"
    }
  }
  ```

---

## 🤖 AI Engine Endpoints (`/ai`)

### `POST /ai/learning-path`
- **Summary**: Generate personalized multi-week career roadmap.
- **Auth**: `Bearer JWT`
- **Request Body**:
  ```json
  {
    "career_goal": "Senior Backend Architect",
    "current_skill_level": "Intermediate",
    "target_timeframe": "6 Weeks"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "career_goal": "Senior Backend Architect",
    "estimated_duration": "6 Weeks",
    "learning_path": [
      {
        "week": 1,
        "topic": "Distributed Systems & FastAPI Microservices",
        "description": "Master async processing, event loops, and database connection pooling.",
        "skills_to_acquire": ["FastAPI", "SQLAlchemy 2.0", "PostgreSQL"]
      }
    ]
  }
  ```

### `GET /ai/provider-status`
- **Summary**: Live diagnostic health status of Groq and Gemini provider chains.
- **Auth**: None
- **Response** (`200 OK`):
  ```json
  {
    "provider": "Groq",
    "model": "llama-3.3-70b-versatile",
    "healthy": true,
    "fallback_models": ["deepseek-r1-distill-llama-70b", "qwen/qwen3-32b"]
  }
  ```

---

## 📚 Knowledge Base (RAG) Endpoints (`/knowledge`)

### `POST /knowledge/upload`
- **Summary**: Upload PDF/TXT document to Enterprise Knowledge Base.
- **Auth**: `Bearer JWT` (`instructor` / `admin`)
- **Response** (`201 Created`):
  ```json
  {
    "document_id": "840082d1-296b-4b26-816b-03d62ffbf562",
    "filename": "Company_Security_Policy_2026.pdf",
    "chunks_ingested": 14,
    "status": "INGESTED"
  }
  ```

---

## 🏥 Health Monitoring Endpoints

### `GET /health/ai`
- **Summary**: Real-time diagnostic check for LLM providers.
- **Auth**: None
- **Response** (`200 OK`):
  ```json
  {
    "current_provider": "Groq",
    "current_model": "llama-3.3-70b-versatile",
    "available_groq_models": ["llama-3.3-70b-versatile", "deepseek-r1-distill-llama-70b"],
    "available_gemini_models": ["models/gemini-3.6-flash", "models/gemini-3.5-flash"],
    "failover_status": "Operational",
    "last_successful_provider": "Groq",
    "last_successful_model": "llama-3.3-70b-versatile",
    "provider_health": {
      "Groq": "Healthy",
      "Gemini": "Healthy"
    }
  }
  ```
