<div align="center">
  <h1>🚀 AI Learning Management Platform</h1>
  <p><strong>Enterprise-Grade, Provider-Agnostic AI-Native Learning & Development Ecosystem</strong></p>

  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
  [![Groq](https://img.shields.io/badge/Groq-F54E00?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
  [![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
  [![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge&logo=database&logoColor=white)](https://www.trychroma.com/)
</div>

---

## 📖 Overview

The **AI Learning Management Platform** is a full-stack, enterprise-ready learning management ecosystem designed to accelerate career growth, automate corporate upskilling, and power intelligent knowledge discovery.

Built on a **Multi-Provider Multi-Model AI Architecture**, the system routes AI generation requests to **Groq** as the Primary Provider (executing multi-model failover chains across Llama, DeepSeek, and Qwen) and seamlessly fails over to **Google Gemini** if Groq models become unavailable. The platform integrates an **Enterprise Retrieval-Augmented Generation (RAG)** pipeline powered by **ChromaDB** and an autonomous **Multi-Agent Workflow Engine**.

---

## ✨ Key Features

- **🌐 Multi-Provider Multi-Model AI Engine**: Executes intra-provider model chains (Groq `llama-3.3-70b-versatile` $\rightarrow$ `deepseek-r1-distill-llama-70b` $\rightarrow$ `qwen/qwen3-32b` $\rightarrow$ `openai/gpt-oss-120b`) before performing inter-provider failover to Google Gemini (`gemini-3.6-flash` $\rightarrow$ `gemini-3.5-flash`).
- **🧠 Personalized Learning Paths**: Automatically curates multi-week roadmaps tailored to employee career goals, current skill levels, and role expectations.
- **📚 Enterprise Knowledge Base (RAG)**: Chat directly with internal documents, policy PDFs, and manuals using hybrid semantic search and vector embeddings in ChromaDB.
- **🤖 Multi-Agent Workflow Engine**: Autonomous AI agents that summarize complex course modules, grade assessments, and curate training materials.
- **🛡️ Enterprise Security**: Role-Based Access Control (RBAC with Student, Instructor, Admin roles), JWT authentication, bcrypt password hashing, and Supabase security.
- **📊 Real-Time Diagnostic Health Monitoring**: Provides live provider/model operational telemetry via `GET /health/ai`.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    Client[Web Browser - React/Vite] -->|REST / JSON| FastAPI[FastAPI Backend Server]

    subgraph Authentication & Security
        FastAPI --> AuthMiddleware[JWT Auth & RBAC Middleware]
        AuthMiddleware --> Postgres[(PostgreSQL / Supabase)]
    end

    subgraph Business Logic & Core Services
        FastAPI --> AIService[AIService Facade]
        FastAPI --> RAGService[RAGService Engine]
        FastAPI --> WorkflowEngine[Multi-Agent Workflow Engine]
    end

    subgraph AI Platform Abstraction Layer
        AIService --> LLMManager[LLMManager Orchestrator]
        RAGService --> LLMManager
        WorkflowEngine --> LLMManager
        LLMManager --> ProviderRegistry[ProviderRegistry]
    end

    subgraph Multi-Model Provider Execution
        ProviderRegistry -->|Primary| GroqProvider[GroqProvider]
        ProviderRegistry -->|Fallback| GeminiProvider[GeminiProvider]
        
        GroqProvider -->|Model Chain 1-5| GroqAPI[Groq Cloud API]
        GeminiProvider -->|Model Chain 1-5| GeminiAPI[Google Gemini API]
    end

    subgraph Vector Knowledge Storage
        RAGService --> ChromaDB[(ChromaDB Vector Store)]
    end
```

---

## 🛠️ Technology Stack

| Layer | Component | Technologies |
| :--- | :--- | :--- |
| **Frontend** | UI & Routing | React 18, Vite, TailwindCSS, React Router V6, Axios, Lucide Icons, Recharts |
| **Backend** | API Framework | Python 3.12+, FastAPI, Pydantic V2, Uvicorn |
| **Database** | Relational DB | PostgreSQL, Supabase Serverless, SQLAlchemy 2.0, Alembic |
| **AI Layer** | Multi-Provider Engine | **Groq SDK / REST**, **Google GenAI SDK**, OpenRouter REST API |
| **Vector Store** | RAG Search | ChromaDB (`hnsw:cosine` embedding space) |
| **Containerization** | Infrastructure | Docker, Docker Compose |

---

## 📂 Folder Structure

```text
.
├── backend/                            # FastAPI Application Root
│   ├── app/
│   │   ├── agents/                     # Multi-Agent Engine & Agent Tools
│   │   ├── ai/                         # Multi-Provider Multi-Model Layer
│   │   │   ├── providers/              # Concrete Provider Implementations
│   │   │   │   ├── base_provider.py    # Abstract Base Class & Failover Exceptions
│   │   │   │   ├── gemini_provider.py  # Gemini Multi-Model Provider
│   │   │   │   ├── groq_provider.py    # Groq Multi-Model Provider
│   │   │   │   └── openrouter_provider.py # OpenRouter Provider
│   │   │   ├── provider_registry.py    # Dynamic Provider Registry
│   │   │   ├── llm_manager.py          # Centralized LLM Failover Orchestrator
│   │   │   ├── ai_service.py           # Business AI Service Facade
│   │   │   ├── prompt_manager.py       # Prompt Templates
│   │   │   └── response_parser.py      # JSON Sanitization & Parsing
│   │   ├── core/                       # Settings & App Config
│   │   ├── database/                   # SQLAlchemy Engine & Models
│   │   ├── rag/                        # Enterprise RAG & ChromaDB Integration
│   │   ├── routers/                    # FastAPI REST Endpoints
│   │   └── schemas/                    # Pydantic Schemas
│   ├── tests/                          # Complete Unit & Integration Test Suite
│   ├── .env.example                    # Environment Configuration Template
│   └── requirements.txt                # Python Dependencies
├── frontend/                           # React + Vite Client Application
│   ├── src/
│   │   ├── components/                 # TopBar, Sidebar, Modals, Cards
│   │   ├── pages/                      # Dashboard, AIAssistant, KnowledgeBase, Admin
│   │   └── services/                   # Axios API Clients & System Services
└── docs/                               # Detailed Enterprise Documentation
    ├── architecture.md                 # System Architecture
    ├── backend.md                      # Backend Specification
    ├── frontend.md                     # Frontend Specification
    ├── provider-architecture.md        # AI Provider Deep Dive
    ├── rag.md                          # Enterprise RAG Engine
    ├── agents.md                       # Multi-Agent Workflow Engine
    ├── authentication.md               # Auth & Security Specifications
    ├── api-reference.md                # Complete API Documentation
    └── deployment.md                  # Deployment Guide
```

---

## ⚙️ Environment Variables

Copy `backend/.env.example` to `backend/.env` and update values:

```env
# Multi-Provider AI Platform Configuration
PRIMARY_PROVIDER=groq
FALLBACK_PROVIDERS=gemini

# Groq Credentials & Models Chain
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODELS=llama-3.3-70b-versatile,deepseek-r1-distill-llama-70b,qwen/qwen3-32b,openai/gpt-oss-120b,llama-3.1-8b-instant

# Gemini Credentials & Models Chain
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODELS=models/gemini-3.6-flash,models/gemini-3.5-flash,models/gemini-flash-latest,models/gemini-3.5-flash-lite,models/gemini-3.1-flash-lite

# AI Execution Retries & Timeouts
AI_TIMEOUT_SECONDS=30.0
AI_MAX_RETRIES=2
AI_BACKOFF_FACTOR=1.5

# Database & Security
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_learning_db
SECRET_KEY=your-super-secret-jwt-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
```

---

## 🚀 Running Locally

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations & start FastAPI server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The application will be accessible at `http://localhost:5173`.

---

## 🧪 Testing

Run the full automated test suite:
```bash
cd backend
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 📚 Detailed Documentation

- 📐 **[System Architecture](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/docs/architecture.md)**
- 🤖 **[Multi-Provider AI Architecture](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/docs/provider-architecture.md)**
- 🔍 **[Enterprise RAG Engine](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/docs/rag.md)**
- 👥 **[Multi-Agent Workflows](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/docs/agents.md)**
- 💾 **[Database Schema & ERD](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/DATABASE.md)**
- 🔐 **[Security & RBAC](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/SECURITY.md)**
- 🌐 **[API Reference](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/docs/api-reference.md)**
- 🚢 **[Deployment Guide](file:///Users/shaiksohel/Downloads/ai-learning-management-platform/DEPLOYMENT.md)**

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.