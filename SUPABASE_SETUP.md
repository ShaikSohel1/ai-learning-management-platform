# Supabase PostgreSQL Integration & Setup Guide

This guide details setting up **Supabase Serverless PostgreSQL** for the **AI Learning Management Platform**.

---

## 🏗️ Overview

Supabase provides the managed PostgreSQL database, authentication services, and Row-Level Security (RLS) storage infrastructure for the platform.

```mermaid
graph TD
    FastAPI[FastAPI Backend Application] -->|SQLAlchemy Engine / SessionPool| SupabasePooler[Supabase Connection Pooler :5432]
    SupabasePooler --> Postgres[(PostgreSQL Serverless DB)]

    subgraph Security & Isolation
        Postgres --> RLS[Row-Level Security Policies]
        Postgres --> Tables[users, courses, enrollments, learning_paths, notifications]
    end
```

---

## 🛠️ Step-by-Step Setup

### Step 1: Create Supabase Project
1. Log in to [Supabase Console](https://supabase.com) and click **New Project**.
2. Set Project Name: `ai-learning-management-platform`.
3. Choose your nearest region (e.g. `ap-northeast-1`).
4. Generate and save a secure Database Password.

---

### Step 2: Retrieve API Keys & Connection Strings

In Supabase Dashboard under **Project Settings $\rightarrow$ Database**:
1. Copy **Connection String (Transaction Pooler)**:
   ```text
   DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres
   ```

In Supabase Dashboard under **Project Settings $\rightarrow$ API**:
2. Copy:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`

---

### Step 3: Run Database Migrations

Use Python SQLAlchemy to automatically provision all tables, indexes, and foreign keys:

```bash
cd backend
export DATABASE_URL="postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"

python3 -c "from app.database.database import engine, Base; import app.models; Base.metadata.create_all(bind=engine)"
```

---

### Step 4: Configure Row-Level Security (RLS) Policies

Run the following SQL snippet in the Supabase SQL Editor to enable RLS:

```sql
-- Enable RLS on users table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own user record
CREATE POLICY "Users can select own row" ON users
    FOR SELECT USING (auth.uid() = id);

-- Enable RLS on enrollments
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;

-- Allow users to view their own enrollments
CREATE POLICY "Users view own enrollments" ON enrollments
    FOR SELECT USING (auth.uid() = user_id);
```

---

### Step 5: Update `backend/.env`

Add the Supabase credentials to your `backend/.env`:

```env
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://[PROJECT_REF].supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
