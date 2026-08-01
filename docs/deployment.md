# Cloud Deployment & Infrastructure Guide

This document provides deployment guidelines for deploying the **AI Learning Management Platform** to production cloud environments (**Render**, **Vercel**, **Supabase**, **ChromaDB**).

---

## 🏗️ Production Architecture Topography

```mermaid
graph TD
    Client[Web Browsers] -->|HTTPS| Vercel[Vercel Frontend]
    Vercel -->|HTTPS REST| Render[Render Backend Container]

    subgraph Render Platform Instance
        Render --> LLMManager[LLMManager Orchestrator]
        Render --> ChromaDB[(Persistent ChromaDB Storage)]
    end

    subgraph Managed Cloud Infrastructure
        Render --> Supabase[(Supabase Serverless Postgres)]
        LLMManager --> GroqCloud[Groq API Cloud]
        LLMManager --> GeminiCloud[Google Gemini Cloud API]
    end
```

---

## 🚀 Environment Configuration Matrix

Ensure all variables are populated in your production environment settings:

```env
PRIMARY_PROVIDER=groq
FALLBACK_PROVIDERS=gemini

GROQ_API_KEY=gsk_...
GROQ_MODELS=llama-3.3-70b-versatile,deepseek-r1-distill-llama-70b,qwen/qwen3-32b,openai/gpt-oss-120b,llama-3.1-8b-instant

GEMINI_API_KEY=AIzaSy...
GEMINI_MODELS=models/gemini-3.6-flash,models/gemini-3.5-flash,models/gemini-flash-latest

AI_TIMEOUT_SECONDS=30.0
AI_MAX_RETRIES=2
AI_BACKOFF_FACTOR=1.5

DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres
SECRET_KEY=your_64_byte_random_secret_hex
```
