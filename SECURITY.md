# Security Overview

Security is a foundational pillar of the AI Learning Management Platform. We enforce strict protocols across data storage, network transfer, and application logic.

---

## 1. Authentication & JWT

We use stateless **JSON Web Tokens (JWT)** for all client-server communication.

- **Algorithm**: `HS256` (HMAC with SHA-256).
- **Expiration**: Access tokens expire quickly (e.g., 30 minutes).
- **Storage**: The frontend stores the token securely and attaches it as a `Bearer` token in the `Authorization` header of Axios requests.
- **Middleware Check**: FastAPI's `Depends(get_current_user)` function intercepts incoming requests, decodes the JWT using the `SECRET_KEY`, and halts execution with `HTTP 401` if invalid or expired.

## 2. Password Hashing

We **never** store plain text passwords.
- **Library**: `passlib` configured with the `bcrypt` algorithm.
- **Salting**: Bcrypt automatically salts passwords upon creation, rendering rainbow table attacks ineffective.
- **Verification**: The `verify_password` utility securely hashes incoming login attempts and compares them in constant time against the database string.

## 3. CORS (Cross-Origin Resource Sharing)

The platform enforces strict CORS policies to prevent unauthorized domains from invoking our API.

- Managed via FastAPI's `CORSMiddleware`.
- **Allowed Origins**: Strictly defined via the `FRONTEND_URLS` environment variable (e.g., `http://localhost:5173`).
- **Credentials**: `allow_credentials=True` is enabled.
- **Methods/Headers**: Configured securely depending on the deployment profile.

## 4. Role-Based Access Control (RBAC)

Authorization is handled via robust dependency injection in FastAPI.

- Roles: `employee`, `manager`, `admin`.
- **Example Implementation**: The `Depends(require_admin)` dependency fetches the user profile from the JWT and ensures their role matches `admin`. If not, a `403 Forbidden` error is returned before the route logic ever executes.

## 5. Secrets Management & Environment Variables

- **No Hardcoded Secrets**: Every sensitive value (Database URL, JWT Secret Key, Google Gemini API Key) is injected at runtime via environment variables.
- **Dotenv**: `python-dotenv` loads these safely in development.
- **Docker**: Secrets are passed securely via Docker Compose environment blocks or production orchestrator secrets managers.

## 6. HTTPS & Network Security

- In production, FastAPI is deployed behind a reverse proxy (e.g., Nginx, AWS ALB, Vercel) that terminates SSL/TLS.
- All connections to the Supabase PostgreSQL database require SSL (`sslmode=require` in the connection URI) to prevent Man-In-The-Middle (MITM) data sniffing.

## 7. AI Prompt Injection Mitigation

- User inputs mapped to Google Gemini prompts are sanitized and strongly typed via Pydantic schemas.
- The multi-agent workflow engine strictly scopes the context window to prevent jailbreaking attempts against the AI features.
