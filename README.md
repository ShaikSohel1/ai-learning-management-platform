<div align="center">
  <h1>🚀 AI Learning Management Platform</h1>
  <p><strong>Next-Generation AI-Native Learning & Development Ecosystem</strong></p>
  
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
  [![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
  [![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

  <br />
</div>

## 📖 Overview

The **AI Learning Management Platform (LMS)** is an enterprise-grade ecosystem designed to revolutionize employee training and upskilling. Powered by **Google Gemini** and **ChromaDB**, the platform provides personalized course recommendations, a Retrieval-Augmented Generation (RAG) knowledge base, and automated Multi-Agent learning workflows.

---

## ✨ Key Features

- **🧠 AI-Powered Recommendations**: Real-time course and skill suggestions tailored to user profiles.
- **📚 Interactive Knowledge Base**: Chat with enterprise documents using a sophisticated RAG pipeline.
- **🛡️ Enterprise Security**: Role-Based Access Control (RBAC), JWT Authentication, and Supabase RLS.
- **📊 Real-Time Analytics**: Built-in charting and metric cards tracking learner progress and skill gaps.
- **🤖 Multi-Agent Architecture**: Autonomous AI agents that summarize lessons, grade assessments, and curate content.
- **🎨 Lovable Aesthetics**: Modern glassmorphism UI, ⌘K search, and dynamic responsive layouts powered by TailwindCSS.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React, Vite, TailwindCSS, React Router, Recharts, Axios, Lucide Icons |
| **Backend** | Python, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic |
| **Database** | PostgreSQL (Supabase Serverless), Redis (Caching) |
| **AI / NLP** | Google Gemini (Gemini 2.0 Flash), ChromaDB (Vector Store), LangChain |
| **Deployment** | Docker, Docker Compose |

---

## 🏗️ Architecture

```mermaid
graph TD
    Client[Web Browser] -->|REST/JSON| FastAPI[FastAPI Backend]
    
    subgraph Backend Services
        FastAPI --> Auth[Auth Service / JWT]
        FastAPI --> API[REST API Endpoints]
        FastAPI --> RAG[RAG Pipeline]
        FastAPI --> Agents[Multi-Agent System]
    
        RAG -->|Vectors| Chroma[(ChromaDB)]
        RAG -->|LLM Prompts| Gemini[Google Gemini API]
        Agents -->|Workflows| Gemini
    end
    
    API --> ORM[SQLAlchemy 2.0]
    Auth --> ORM
    
    ORM --> Supabase[(Supabase PostgreSQL)]
```

---

## 📂 Folder Structure

See the complete [Project Structure Documentation](docs/PROJECT_STRUCTURE.md) for details.

```text
.
├── backend/            # FastAPI Application
│   ├── app/            # Core logic, models, schemas, routers, and services
│   ├── alembic/        # Database migrations
│   ├── chroma_db/      # Local ChromaDB persistent storage (Ignored by Git)
│   └── tests/          # Pytest suites
├── frontend/           # React/Vite Application
│   ├── src/            # UI components, contexts, pages, and API handlers
│   └── public/         # Static assets
└── docs/               # Technical Documentation
```

---

## 🔒 Authentication Flow

1. User submits credentials to `POST /auth/login`.
2. FastAPI validates against Supabase PostgreSQL using `passlib/bcrypt`.
3. An encrypted **JWT Access Token** is generated and returned.
4. The React Frontend attaches the token via an Axios Interceptor (`Authorization: Bearer <token>`).
5. FastAPI verifies the token via `get_current_user` dependencies on protected routes.

---

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (3.11+)
- Docker & Docker Compose
- Supabase Project & Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/ShaikSohel1/ai-learning-management-platform.git
cd ai-learning-management-platform
```

### 2. Environment Variables
Copy `.env.example` to `.env` in both the `frontend` and `backend` directories.

**`backend/.env`**
```ini
DATABASE_URL="postgresql://postgres.[YOUR_REF]:[YOUR_PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require"
SECRET_KEY="your-super-secret-jwt-key"
GEMINI_API_KEY="your-google-gemini-key"
FRONTEND_URLS="http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174"
```

**`frontend/.env`**
```ini
VITE_API_URL="http://localhost:8000"
```

### 3. Run the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### 4. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📸 Screenshots

| Dashboard | AI Knowledge Base |
| :---: | :---: |
| ![Dashboard](docs/assets/dashboard_placeholder.png) | ![AI Knowledge Base](docs/assets/ai_kb_placeholder.png) |

---

## 📚 Comprehensive Documentation

For deep dives into specific system components, review our dedicated docs:

- [API Reference](docs/API.md)
- [Database Schema & ERD](DATABASE.md)
- [AI Assistant & RAG](docs/AI_ASSISTANT.md)
- [Architecture Details](docs/ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Supabase Setup Guide](SUPABASE_SETUP.md)
- [Security Model](SECURITY.md)
- [Migration Guide](MIGRATION_GUIDE.md)

---

## 🤝 Contributing

We welcome contributions from the Open Source community! Please read our [Contributing Guide](docs/CONTRIBUTING.md) for details on our code of conduct, pull request process, and development standards.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Shaik Sohel**
- GitHub: [@ShaikSohel1](https://github.com/ShaikSohel1)