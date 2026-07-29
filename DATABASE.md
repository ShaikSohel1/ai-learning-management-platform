# Database Architecture & Management

The AI Learning Management Platform uses **PostgreSQL (Supabase)** as its core relational database. The application interacts with the database entirely via **SQLAlchemy ORM**.

## 1. ORM and Migrations
- **SQLAlchemy Models**: All models are defined in `backend/app/models/`. These map directly to database tables (e.g., `users`, `courses`, `enrollments`).
- **Alembic**: We use Alembic to handle schema migrations. The configuration is stored in `backend/alembic.ini` and `backend/alembic/env.py`.

### Migration Commands
Whenever you make changes to a model in `app/models/`, run the following commands to sync the database:
```bash
# Generate a new migration script
alembic revision --autogenerate -m "Description of change"

# Apply the migration to the database
alembic upgrade head
```

## 2. Connection Pooling
To ensure high performance and prevent database connection exhaustion, `backend/app/database/database.py` is configured with:
- `pool_size=10`: Keeps 10 connections open per worker.
- `max_overflow=20`: Allows up to 20 additional connections during spikes.
- `pool_pre_ping=True`: Verifies a connection is active before using it, preventing stale connection errors.

## 3. Storage
Files (PDFs, Profile Pictures, Certificates) are stored in **Supabase Storage**.
- The `backend/app/services/storage_service.py` handles communication with the Supabase Storage API using the official `supabase-py` client.
- The default bucket used is `main-bucket`.

## 4. Rollback Steps
If a database migration causes issues in production:
1. Identify the previous stable revision ID (`alembic history`).
2. Run `alembic downgrade [REVISION_ID]`.
3. Revert your code changes to match the database schema.
