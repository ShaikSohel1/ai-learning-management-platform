# Project Structure

The repository is divided into clear functional boundaries, predominantly split between the `frontend/` (React) and `backend/` (FastAPI) ecosystems.

```text
ai-learning-management-platform/
│
├── backend/                        # 🐍 FastAPI Backend Application
│   ├── alembic/                    # Database migration tracking
│   │   ├── versions/               # Auto-generated SQL diffs
│   │   └── env.py                  # Migration execution environment
│   │
│   ├── app/                        # Application Source Code
│   │   ├── agents/                 # Autonomous AI Workflow Logic
│   │   ├── ai/                     # Gemini SDK Client & Prompt Managers
│   │   ├── core/                   # Global Configs, JWT, & Logging
│   │   ├── database/               # SQLAlchemy Engine & Session generation
│   │   ├── dependencies/           # FastAPI Injection (Auth & RBAC)
│   │   ├── models/                 # SQLAlchemy ORM Classes (Tables)
│   │   ├── rag/                    # Retrieval Augmented Generation logic
│   │   ├── routers/                # API Endpoints (Controllers)
│   │   ├── schemas/                # Pydantic Types (Validation DTOs)
│   │   └── services/               # Core Business Logic (CRUD & integrations)
│   │
│   ├── chroma_db/                  # Vector DB Storage (Ignored in Git)
│   ├── tests/                      # Pytest Suites for unit testing
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Template for environment variables
│   └── alembic.ini                 # Alembic configuration
│
├── frontend/                       # ⚛️ React & Vite Frontend Application
│   ├── public/                     # Static assets (Favicons, manifest)
│   ├── src/                        # Source Code
│   │   ├── assets/                 # Images and SVGs
│   │   ├── components/             # Reusable UI elements (Buttons, Cards)
│   │   ├── context/                # React Contexts (AuthContext)
│   │   ├── pages/                  # Route-level components (Dashboard, Login)
│   │   ├── services/               # Axios API clients
│   │   ├── App.jsx                 # Application entry and React Router
│   │   ├── index.css               # Tailwind directives and Global CSS
│   │   └── main.jsx                # React DOM binding
│   │
│   ├── package.json                # NPM Scripts and dependencies
│   ├── tailwind.config.js          # Tailwind theme and plugin config
│   └── vite.config.js              # Vite build configurations
│
├── docs/                           # 📚 Comprehensive Documentation
│   ├── API.md                      # REST Endpoint docs
│   ├── ARCHITECTURE.md             # System design docs
│   ├── AI_ASSISTANT.md             # RAG and Agent docs
│   └── PROJECT_STRUCTURE.md        # This file
│
├── docker-compose.yml              # Container orchestration
├── README.md                       # Main repository landing page
├── DEPLOYMENT.md                   # Environment setup guides
├── DATABASE.md                     # Schema definitions and ERD
├── SECURITY.md                     # Authorization and InfoSec rules
├── SUPABASE_SETUP.md               # DB configuration instructions
└── MIGRATION_GUIDE.md              # Historical database migration notes
```

### Key Conventions

- **Separation of Concerns (Backend)**: Do not write database queries directly in the `routers/`. Routers handle HTTP translation, while `services/` handle the actual business logic.
- **Component Reusability (Frontend)**: Small, generic UI elements belong in `src/components/`, while page-specific assemblies belong in `src/pages/`.
