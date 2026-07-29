# Deployment Guide

This guide details how to deploy the AI Learning Management Platform into production, specifically focusing on the backend FastAPI server and React Vite frontend.

## 1. Prerequisites
- A live Supabase project.
- Accounts on deployment platforms (e.g., Render, Railway, Fly.io for Backend; Vercel or Netlify for Frontend).
- Access to the platform's Environment Variables settings.

## 2. Backend Deployment (Render / Railway)

### Environment Variables
Configure the following secrets in your deployment dashboard:
- `DATABASE_URL`: Your Supabase connection string (ensure it uses port 6543 for pooling).
- `SECRET_KEY`: A strong, randomly generated string for JWT signing.
- `ALGORITHM`: `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30` (or your preferred duration)
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `SUPABASE_URL`: Your Supabase Project URL.
- `SUPABASE_ANON_KEY`: Your Supabase public anon key.
- `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase private service role key.

### Build & Run Commands
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Database Migrations
Before handling real traffic, ensure your database schema is up to date. You can run migrations locally pointing to your production database, or add a pre-deploy script to your CI/CD pipeline:
```bash
alembic upgrade head
```

## 3. Frontend Deployment (Vercel)

### Environment Variables
Configure the following in Vercel:
- `VITE_API_URL`: The public URL of your deployed backend (e.g., `https://my-backend.onrender.com`).

### Build Settings
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

## 4. Supabase Connection Pooling
Your `database.py` is pre-configured with `pool_size` and `max_overflow`. Ensure your `DATABASE_URL` connects to Supabase via IPv4 (port `6543`) using PgBouncer to prevent connection limits from being exhausted in serverless or highly concurrent environments.
