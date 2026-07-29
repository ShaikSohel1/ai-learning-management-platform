# Supabase Setup Guide

This project leverages Supabase as the primary PostgreSQL database and object storage provider.

---

## 1. Project Creation

1. Go to [Supabase](https://supabase.com/) and create an account.
2. Click **New Project**, select an organization, and choose a deployment region close to your primary user base.
3. Provide a strong **Database Password**. *Store this safely, as you will need it for the connection string.*

---

## 2. API Keys & Connection Strings

Once the project is provisioned, navigate to **Project Settings -> Database**.

You will need the **Connection String (URI)**. For FastAPI / SQLAlchemy, it is crucial to use the **Session Pooler** string rather than the direct connection.

- **Standard Pooler Connection**:
  ```ini
  DATABASE_URL="postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require"
  ```
- *Note the port `6543` which routes through PgBouncer, preventing connection exhaustion from the FastAPI workers.*

Save this string to your `backend/.env` file.

---

## 3. Database Migration (Alembic)

Do NOT manually create tables in the Supabase SQL editor. The schema is entirely defined by SQLAlchemy and managed by Alembic.

To push the schema to your fresh Supabase project:
```bash
cd backend
alembic upgrade head
```
This will automatically construct all 12+ tables (`users`, `courses`, `enrollments`, etc.).

---

## 4. Authentication (JWT vs Supabase Auth)

**Important Architecture Note**: 
This project uses **FastAPI + JWT Authentication (passlib/bcrypt)**, storing passwords directly in the `users` table as `hashed_password`. 
We **do not** use Supabase Auth (`auth.users`) for this application to maintain strict separation of concerns and allow custom RBAC logic natively in FastAPI.

---

## 5. Storage (Optional)

If your platform needs to handle user avatars, course thumbnails, or PDF certificates, you should set up Supabase Storage:
1. Navigate to **Storage** in the Supabase dashboard.
2. Create a new bucket (e.g., `learning-assets`).
3. Make the bucket **Public** if serving images directly to the frontend.
4. Retrieve the `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from the Project Settings -> API to allow FastAPI to upload objects via the `supabase-py` client.

---

## 6. Row Level Security (RLS)

Because the FastAPI backend connects to Supabase using a standard PostgreSQL URI as an admin/superuser role, **Row Level Security (RLS) is bypassed by default** for backend queries. 

All access control, role verification (`admin`, `manager`, `employee`), and data masking is handled explicitly by the **FastAPI Dependency Injection** layer (e.g., `get_current_user`, `require_admin`).
