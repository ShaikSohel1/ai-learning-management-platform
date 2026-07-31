from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    document_id: str = Field(..., description="Unique document identifier UUID")
    document_name: str = Field(..., description="File name of the uploaded document")
    upload_date: str = Field(..., description="ISO timestamp of upload")
    uploaded_by: str = Field(..., description="Name or email of uploader")
    chunk_count: int = Field(..., description="Total text chunks extracted")
    embedding_count: int = Field(..., description="Total vector embeddings generated")
    document_size: str = Field(..., description="Human readable file size (e.g. '120 KB')")


class KnowledgeAskRequest(BaseModel):
    question: str = Field(..., min_length=3, description="User question for RAG knowledge base", json_schema_extra={"example": "What is the employee leave policy?"})
    top_k: int | None = Field(4, ge=1, le=10, description="Top K relevant chunks to retrieve")
    threshold: float | None = Field(0.3, ge=0.0, le=1.0, description="Minimum similarity confidence threshold")


class KnowledgeCitation(BaseModel):
    document_name: str = Field(..., description="Source document filename")
    chunk_index: int = Field(..., description="Chunk index within source document")
    similarity_score: float = Field(..., description="Confidence score (0.0 to 1.0)")
    snippet: str = Field(..., description="Excerpt text snippet from source document")


class KnowledgeAskResponse(BaseModel):
    answer: str = Field(..., description="AI response generated using RAG context or Gemini fallback")
    rag_used: bool = Field(..., description="True if RAG document context was retrieved and used")
    confidence_score: float = Field(..., description="Overall confidence percentage (0.0 to 100.0%)")
    response_time_ms: float = Field(..., description="Execution latency in milliseconds")
    search_intent: str = Field(..., description="Detected query intent (policy, procedure, technical, general)")
    citations: list[KnowledgeCitation] = Field(default_factory=list, description="Source document citations")
    referenced_documents: list[str] = Field(default_factory=list, description="List of unique source document titles")


class SemanticSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Search query string")
    top_k: int | None = Field(4, ge=1, le=20)
    threshold: float | None = Field(0.3, ge=0.0, le=1.0)
    filename_filter: str | None = Field(None, description="Optional filename filter")


class KnowledgeSearchResponse(BaseModel):
    query: str
    results_count: int
    confidence_score: float
    search_intent: str
    citations: list[KnowledgeCitation]


class SearchHistoryItem(BaseModel):
    entry_id: str
    user_id: int
    question: str
    timestamp: str
    response_time_ms: float
    documents_used: list[str]
    confidence_score: float
    rag_used: bool


class KnowledgeAnalyticsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    avg_chunk_size_chars: int
    total_embeddings: int
    avg_response_time_ms: float
    avg_confidence_score: float
    rag_utilization_rate: float
    knowledge_base_size_bytes: str
