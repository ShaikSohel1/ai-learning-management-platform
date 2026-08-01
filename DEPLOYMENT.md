# Production Deployment Guide

This guide details the step-by-step instructions for deploying the **AI Learning Management Platform** to production environments, including **Render** (FastAPI Backend), **Vercel** (React Frontend), **Supabase** (PostgreSQL Database), and persistent **ChromaDB** storage.

---

## 🏗️ Production Infrastructure Topography

```mermaid
graph TD
    Client[Users / Browsers] -->|HTTPS| Vercel[Vercel Frontend - React 18 / Vite]
    Vercel -->|HTTPS REST API| Render[Render Backend - FastAPI Service]

    subgraph Render Cloud Instance
        Render --> LLMManager[LLMManager Orchestrator]
        Render --> ChromaDB[(Persistent ChromaDB Storage)]
    end

    subgraph Managed Cloud Infrastructure
        Render -->|PostgreSQL Connection Pool| Supabase[(Supabase Serverless Postgres)]
        LLMManager -->|Primary Model Chain| GroqAPI[Groq API Cloud]
        LLMManager -->|Fallback Model Chain| GeminiAPI[Google Gemini API]
    end
```

---

## 1. Supabase Database Provisioning

1. Log in to [Supabase Console](https://supabase.com) and create a new project.
2. Under **Project Settings $\rightarrow$ Database**, retrieve your connection URI:
   ```text
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres
   ```
3. Under **Project Settings $\rightarrow$ API**, retrieve:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
4. Execute initial database schema migrations using SQLAlchemy:
   ```bash
   cd backend
   DATABASE_URL="your-supabase-url" python3 -c "from app.database.database import engine, Base; import app.models; Base.metadata.create_all(bind=engine)"
   ```

---

## 2. Render Backend Deployment

1. Create a new **Web Service** on [Render Console](https://render.com).
2. Connect your Git repository and set build options:
   - **Environment**: Python 3.12+
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
3. Configure persistent disk storage for ChromaDB:
   - Mount Path: `/app/chroma_db`
   - Size: 10 GB
4. Set Environment Variables in Render Dashboard:

| Variable | Recommended Value | Description |
| :--- | :--- | :--- |
| `PRIMARY_PROVIDER` | `groq` | Primary LLM Provider |
| `FALLBACK_PROVIDERS` | `gemini` | Fallback LLM Provider chain |
| `GROQ_API_KEY` | `gsk_...` | Production Groq API Key |
| `GROQ_MODELS` | `llama-3.3-70b-versatile,deepseek-r1-distill-llama-70b,qwen/qwen3-32b,openai/gpt-oss-120b` | Groq Model chain |
| `GEMINI_API_KEY` | `AIzaSy...` | Production Google Gemini API Key |
| `GEMINI_MODELS` | `models/gemini-3.6-flash,models/gemini-3.5-flash,models/gemini-flash-latest` | Gemini Model chain |
| `AI_TIMEOUT_SECONDS` | `30.0` | Execution timeout per model request |
| `AI_MAX_RETRIES` | `2` | Max backoff retries per model |
| `DATABASE_URL` | `postgresql://...` | Supabase Postgres URI |
| `SECRET_KEY` | `[RANDOM_64_CHAR_HEX_STRING]` | Production JWT Secret Key |
| `ALGORITHM` | `HS256` | JWT Algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token expiration duration |

---

## 3. Vercel Frontend Deployment

1. Import your project into [Vercel Console](https://vercel.com).
2. Set directory settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Configure Environment Variables:
   ```env
   VITE_API_BASE_URL=https://your-render-backend.onrender.com
   ```
4. Deploy the project.

---

## 4. Production Health Checks & Diagnostics

After deployment, verify system health using the built-in diagnostic endpoints:

### 1. Multi-Provider AI Health Check
```bash
curl -X GET https://your-backend.onrender.com/health/ai
```
**Expected Response**:
```json
{
  "current_provider": "Groq",
  "current_model": "llama-3.3-70b-versatile",
  "available_groq_models": [
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b",
    "qwen/qwen3-32b",
    "openai/gpt-oss-120b"
  ],
  "available_gemini_models": [
    "models/gemini-3.6-flash",
    "models/gemini-3.5-flash",
    "models/gemini-flash-latest"
  ],
  "failover_status": "Operational",
  "last_successful_provider": "Groq",
  "last_successful_model": "llama-3.3-70b-versatile",
  "provider_health": {
    "Groq": "Healthy",
    "Gemini": "Healthy"
  }
}
```

### 2. Full System Diagnostic Status
```bash
curl -X GET https://your-backend.onrender.com/status
```

---

## 📋 Production Readiness Checklist

- [x] `PRIMARY_PROVIDER` configured to `groq` and `GROQ_API_KEY` validated.
- [x] `GEMINI_API_KEY` set as fallback provider.
- [x] CORS configuration updated with Vercel frontend production URL.
- [x] `SECRET_KEY` replaced with strong 64-byte random string.
- [x] Persistent volume mounted on `/app/chroma_db` for ChromaDB vector store.
- [x] PostgreSQL connection pool configured and verified on Supabase.
- [x] All 31 automated unit tests passing (`PYTHONPATH=backend python3 -m unittest discover -s backend/tests -p "test_*.py"`).
