# High-Level System Architecture

This document provides a architectural specification of the **AI Learning Management Platform**.

---

## 🏗️ System Component Architecture

```mermaid
graph TD
    subgraph Frontend Layer React 18 / Vite
        UI[User Interface Components] --> Router[React Router V6]
        Router --> Views[Dashboard / AIAssistant / KnowledgeBase / Admin]
        Views --> APIService[Axios API Client Services]
    end

    subgraph API Gateway Layer FastAPI
        APIService -->|HTTPS REST| MainAPI[FastAPI Application Router]
        MainAPI --> AuthMiddleware[JWT Authentication Middleware]
        MainAPI --> CORSMiddleware[CORS Security Filter]
    end

    subgraph Service Layer Python 3.12+
        MainAPI --> AIService[AIService Facade]
        MainAPI --> RAGService[Enterprise RAG Search Engine]
        MainAPI --> WorkflowEngine[Multi-Agent Workflow Engine]
        MainAPI --> AuthService[Auth & Token Service]
    end

    subgraph Data & Storage Layer
        AuthService --> SQLAlchemy[SQLAlchemy 2.0 ORM]
        SQLAlchemy --> Postgres[(Supabase PostgreSQL Serverless)]
        RAGService --> VectorDB[(ChromaDB Vector Store)]
    end

    subgraph Multi-Provider AI Engine
        AIService --> LLMManager[LLMManager Orchestrator]
        RAGService --> LLMManager
        WorkflowEngine --> LLMManager
        
        LLMManager --> GroqProvider[GroqProvider]
        LLMManager --> GeminiProvider[GeminiProvider]

        GroqProvider --> GroqAPI[Groq API Cloud]
        GeminiProvider --> GeminiAPI[Google Gemini Cloud API]
    end
```

---

## 🔄 End-to-End User Interaction Flow

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant React as React Client
    participant API as FastAPI Backend
    participant RAG as RAGService
    participant LLM as LLMManager
    participant DB as PostgreSQL DB

    Student->>React: Submit Knowledge Query / Chat Prompt
    React->>API: POST /ai/chat (Bearer JWT)
    API->>API: Verify JWT Token & User Permissions
    API->>RAG: search_relevant_chunks(query)
    RAG-->>API: Return top N context chunks (cosine similarity)
    API->>LLM: generate_content(prompt + context)
    LLM->>LLM: Try Groq models -> Gemini fallbacks
    LLM-->>API: Return synthesized AI answer
    API->>DB: Log conversation history
    API-->>React: 200 OK (Response text + citations)
    React-->>Student: Display AI answer with source citations
```
