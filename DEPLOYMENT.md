# Deployment Guide

This guide covers deploying the AI Learning Management Platform for both Local Development and Production environments.

---

## 💻 Local Development

### 1. Prerequisites
- **Node.js** (v18 or higher)
- **Python** (3.11 or higher)
- **Docker & Docker Compose** (Optional, but recommended)
- **PostgreSQL** (Or an active Supabase project)

### 2. Environment Setup

**Backend (`backend/.env`)**:
```ini
DATABASE_URL="postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]?sslmode=require"
SECRET_KEY="generate-a-strong-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"

# AI Integration
GEMINI_API_KEY="your_google_gemini_api_key"

# CORS Configuration
FRONTEND_URLS="http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174"
```

**Frontend (`frontend/.env`)**:
```ini
VITE_API_URL="http://127.0.0.1:8000"
```

### 3. Running Services

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

---

## 🐳 Docker Deployment

To spin up the entire stack seamlessly, you can use the provided `docker-compose.yml`.

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f
```
*Note: Make sure your `.env` files are correctly configured in both the root and child directories before running Docker.*

---

## 🚀 Production Deployment

### 1. Backend (FastAPI)
The backend is completely containerized and stateless (aside from ChromaDB, which should mount a persistent volume).

- **Host**: AWS EC2, Google Cloud Run, or Render.
- **Run Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
  ```
- **ChromaDB**: In production, consider hosting ChromaDB as a separate microservice rather than embedding it, to allow the FastAPI workers to scale horizontally.

### 2. Frontend (React/Vite)
- Build the static assets:
  ```bash
  cd frontend
  npm run build
  ```
- **Host**: Vercel, Netlify, or AWS S3 + CloudFront.
- Ensure that the build environment variable `VITE_API_URL` points to your production FastAPI domain (e.g., `https://api.yourdomain.com`).

### 3. Database (Supabase)
- The database is managed entirely by Supabase Serverless Postgres.
- Ensure your `DATABASE_URL` uses the **Session Pooler** string (typically port `6543`) to prevent connection exhaustion from FastAPI workers.

---

## ⚠️ Troubleshooting

**1. CORS Errors (400 Bad Request)**
- If the frontend fails to communicate with the backend, verify that the frontend origin is exactly matched in the `FRONTEND_URLS` environment variable in the backend.

**2. Alembic Empty Migrations**
- Ensure that `alembic/env.py` has imported `app.models` so that `Base.metadata` can discover the tables.

**3. ChromaDB SQLite Errors**
- Do NOT track `backend/chroma_db/chroma.sqlite3` in Git. It will cause merge conflicts. It is automatically generated at runtime.
