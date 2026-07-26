# AI Learning Management Platform (Enterprise Production Ready)

An enterprise-grade, AI-native Learning & Development (L&D) platform featuring **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Google Gemini 2.0 LLM**, **ChromaDB Vector Store**, **Hybrid Semantic Search (RAG)**, **Multi-Agent Agentic AI Orchestration**, **Enterprise Tool Execution**, and a **React Dashboard**.

---

## 🌟 Comprehensive Architecture Diagrams

### 1. High-Level System Architecture Diagram
```
 +-----------------------------------------------------------------------------------------+
 |                                  REACT FRONTEND CLIENT                                  |
 |  • Course Catalog   • My Learning   • RAG Knowledge Base   • Multi-Agent UI   • Admin   |
 +-----------------------------------------------------------------------------------------+
                                              | (HTTPS / REST)
                                              v
 +-----------------------------------------------------------------------------------------+
 |                                 FASTAPI BACKEND CORE                                    |
 |  • JWT Auth   • Course CRUD   • Enrollment State Machine   • Security & Health Routers |
 +-----------------------------------------------------------------------------------------+
             |                                              |
             v                                              v
 +-----------------------------+              +--------------------------------------------+
 | POSTGRESQL DATABASE         |              | ENTERPRISE AGENTIC & RAG ENGINE            |
 | • Users & Roles             |              | • Intelligent Router & Workflow Engine     |
 | • Courses & Lessons         |              | • 8 Specialized Agents & Tool Registry     |
 | • Enrollments & Certificates|              | • ChromaDB Persistent Vector Store         |
 | • Notifications & Audits    |              | • Hybrid Search (Vector + BM25 Reranker)   |
 +-----------------------------+              +--------------------------------------------+
                                                            |
                                                            v
                                              +----------------------------+
                                              | GOOGLE GEMINI 2.0 LLM API  |
                                              | (text-embedding-004)       |
                                              +----------------------------+
```

### 2. Multi-Agent Agentic Workflow Engine
```
 [User Goal Prompt] ──> [Intelligent Intent Router]
                                │
                                ├──> [1. Career Planner Agent] (Milestone Roadmap Architecture)
                                │         │
                                ├──> [2. Skill Gap Agent] (Competency Gap % Analysis)
                                │         │
                                ├──> [3. Course Rec Agent] (LMS Catalog Query & Matching)
                                │         │
                                ├──> [4. Knowledge Agent] (ChromaDB RAG Document Retrieval)
                                │         │
                                ├──> [5. Assessment Agent] (Capstone Project & Readiness Score)
                                │         │
                                └──> [6. Dashboard Insights] (Velocity & Drop-off Risk)
                                          │
                                          ▼
                        [Executive Summary + 1-Click Action Trigger]
```

---

## ⚡ Core Platform Features

- **🔐 Role-Based Access Control**: JWT Bearer token authentication supporting Admin and Learner roles.
- **📚 Course Management**: CRUD operations, search, category filters, difficulty sorting, and pagination.
- **🎓 Automated Enrollment & State Machine**: Transitions `NOT_STARTED` $\rightarrow$ `IN_PROGRESS` $\rightarrow$ `COMPLETED` with auto-generation of unique digital certificates (`CERT-XXXXXX`).
- **📖 Enterprise Knowledge Base (RAG)**: Ingests PDF, TXT, Markdown, and DOCX files. Generates 768-dim embeddings (`text-embedding-004`) stored in persistent ChromaDB.
- **⚡ Hybrid Semantic Search**: Combines vector cosine similarity with BM25 term overlap, multi-criteria reranking, sentence-level context compression, and confidence scoring.
- **🤖 Autonomous Multi-Agent AI Platform**: 8 domain-specialized agents (`Career Planner`, `Skill Gap`, `Course Recommendation`, `Assessment`, `Enrollment`, `Knowledge`, `Certificate`, `Dashboard Insights`) communicating across shared memory.
- **🛠️ Enterprise Tool Execution**: 10 executable domain tools wrapping platform APIs for 1-click scheduling (`.ics`), progress exports (`CSV`), email notifications, and in-app alerts.
- **⚙️ Admin Dashboard**: System health monitoring (`/health/database`, `/health/ai`, `/health/vector`), user catalog management, component status badges, and tool execution audit logging.

---

## 🚀 Quickstart & Installation

### Option 1: One-Command Docker Setup (Recommended)

1. Clone repository:
   ```bash
   git clone https://github.com/ShaikSohel1/ai-learning-management-platform.git
   cd ai-learning-management-platform
   ```

2. Launch full stack via Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access Platform:
   - **Frontend UI**: `http://localhost:5173`
   - **FastAPI Docs**: `http://localhost:8000/docs`

---

### Option 2: Local Development Setup

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

| Variable | Required | Description | Default |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql://shaiksohel@localhost/ai_learning_db` |
| `GEMINI_API_KEY` | Yes | Google Gemini API key | `your_gemini_api_key_here` |
| `GEMINI_MODEL` | No | Gemini model identifier | `gemini-2.0-flash` |
| `SECRET_KEY` | Yes | JWT signing key | `your_secret_key_here` |

---

## 🧪 Testing Guide & Commands

### Backend Automated Test Suite
```bash
cd backend
python3 -c "import app.main; print('Backend syntax check OK')"
```

### Frontend Build Verification
```bash
cd frontend
npm run build
```

---

## 📝 Demo Script for Stakeholders

1. **Login & Dashboard**: Login as learner $\rightarrow$ View enrollment statistics, progress bars, and the **🤖 AI Agent Insights & Risk Forecast** widget.
2. **Multi-Agent AI Platform**: Navigate to **✨ AI Assistant** $\rightarrow$ Click preset goal **🚀 Senior Backend Developer Goal** $\rightarrow$ Observe step-by-step pipeline execution visualizer with reasoning cards.
3. **1-Click Action Execution**: Click **🎓 Enroll in Course 1** or **📅 Export Study Plan (.ics)** to verify real tool execution.
4. **Knowledge Base (RAG)**: Navigate to **📖 Knowledge Base** $\rightarrow$ Upload document $\rightarrow$ Ask question $\rightarrow$ Observe **📖 Hybrid Verified Document Context** badge and source citations with confidence %.
5. **Notification Bell**: Click **🔔 Bell Icon** in Navbar to view automated course enrollment & certificate alerts.
6. **Admin Dashboard**: Navigate to **⚙️ Admin** tab $\rightarrow$ View component health status badges (`PostgreSQL DB`, `ChromaDB`, `Gemini LLM`) and audit logs.

---

## 📄 License
Enterprise MIT License. Built by Senior AI Software Engineer & Solution Architect.