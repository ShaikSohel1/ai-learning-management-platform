# AI Assistant & RAG Knowledge Base

The AI Learning Management Platform heavily leverages generative AI to provide dynamic, intelligent experiences for learners.

---

## 🧠 Google Gemini Integration

The core generative engine is **Google Gemini** (specifically utilizing models like `gemini-2.5-flash` for high-throughput responses).

- **Library**: `google-generativeai` python SDK.
- **Service Registration**: `backend/app/ai/gemini_client.py` handles authentication via the `GEMINI_API_KEY` and exposes a robust async interface for generating content.
- **Failovers**: A custom `retry_handler.py` catches `ResourceExhausted` (429) and `InternalServerError` (500) exceptions from Google's API, applying exponential backoff to ensure high availability.

---

## 📚 Retrieval-Augmented Generation (RAG)

Standard LLMs lack context about private corporate documents. We solve this using a RAG pipeline.

### 1. Document Ingestion
When new training materials (PDFs, Markdown, Docx) are uploaded:
1. `document_loader.py` extracts raw text.
2. `text_chunker.py` splits the text into ~1000-token chunks with a 200-token overlap, ensuring semantic boundaries aren't broken.
3. `embedding_service.py` converts these text chunks into dense high-dimensional vectors.

### 2. ChromaDB Vector Store
We use **ChromaDB** as our local vector database (stored in `backend/chroma_db`).
- **Why ChromaDB?** It runs locally alongside the FastAPI application via SQLite bindings, removing the need for a separate costly SaaS vector database.
- *Note: `chroma.sqlite3` is dynamically generated at runtime and strictly excluded from Git tracking.*

### 3. Query Processing
When a user asks the AI Knowledge Base a question:
1. The user's query is vectorized.
2. `vector_store.py` performs a K-Nearest-Neighbors (KNN) search in ChromaDB to find the top 5 most relevant document chunks.
3. `rag_service.py` constructs a complex prompt containing both the user's question and the retrieved chunks.
4. Gemini generates a grounded response.

---

## 🤖 Multi-Agent System

Found in `backend/app/agents/`, the platform utilizes a Multi-Agent architecture where AI agents simulate complex workflows.

- **Agent Manager**: Orchestrates multiple specialized agents (e.g., `CourseCuratorAgent`, `SupportAgent`, `GraderAgent`).
- **Tool Registry**: Agents are equipped with specific tools, allowing them to autonomously fetch database records or trigger side-effects (like emailing a user).
- **Workflow Engine**: Manages the multi-turn conversational loops between the LLM and the tools until a task is completely resolved.
