# Migration Guide: Local PostgreSQL to Supabase

This document outlines the architectural shift from a local instance of PostgreSQL to **Supabase Serverless PostgreSQL** and how to verify the migration.

---

## 1. Context and Motivation

The AI Learning Management Platform originally relied on a local PostgreSQL container for development and testing. To prepare for production scaling, reduce infrastructure overhead, and leverage edge-native features, the database layer was migrated to Supabase.

**Key Constraints Respected During Migration**:
- **No application rewrites**: The backend FastAPI logic and frontend API contracts remained 100% untouched.
- **ORM Preservation**: SQLAlchemy 2.0 remains the sole database interaction layer. `supabase-py` is NOT used for standard CRUD operations.
- **Authentication Preservation**: We maintain our custom JWT implementation rather than replacing it with Supabase Auth.

---

## 2. Configuration Changes

The migration was entirely driven by environment variables and connection strings.

**Old Configuration (Local)**:
```ini
DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_lms"
```

**New Configuration (Supabase)**:
```ini
DATABASE_URL="postgresql://postgres.[REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require"
```
*Note: The Supabase connection uses port 6543 (Session Pooler) to manage database connections efficiently across FastAPI worker threads.*

---

## 3. Alembic Registration Fix

During the migration, a common issue occurs where Alembic auto-generates empty schema migrations. 

To resolve this, we ensure that **all SQLAlchemy models** are imported into `alembic/env.py` before Alembic evaluates `target_metadata = Base.metadata`.

```python
# In alembic/env.py
from app.database.base import Base

# FIX: Explicitly import the models registry
import app.models

target_metadata = Base.metadata
```
This forces Python to evaluate all `DeclarativeBase` subclasses, hydrating `Base.metadata` with the full 12+ table schema before comparing it against the fresh Supabase database.

---

## 4. Execution & Verification Steps

To perform the migration on a fresh clone of the repository:

1. Update `backend/.env` with your Supabase credentials.
2. Initialize Alembic:
   ```bash
   alembic revision --autogenerate -m "Migrate to Supabase"
   ```
3. Verify the generated python file in `alembic/versions/` contains actual `op.create_table()` directives, not an empty `upgrade()` function.
4. Push to Supabase:
   ```bash
   alembic upgrade head
   ```
5. **Verify**: Open the Supabase Dashboard UI, navigate to the **Table Editor**, and confirm all tables (`users`, `courses`, `enrollments`, etc.) are present and properly configured.
