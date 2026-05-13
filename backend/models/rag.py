"""Pydantic models for RAG operations"""

from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentMetadata(BaseModel):
    """Metadata for a document chunk"""
    source: str = Field(..., description="Source file name")
    topic: Optional[str] = Field(None, description="Topic or category")
    framework: Optional[str] = Field(None, description="Framework or language")
    difficulty: Optional[str] = Field(None, description="Difficulty level")
    chunk_index: int = Field(..., description="Chunk index in document")

class DocumentChunk(BaseModel):
    """A chunk of document content with metadata"""
    content: str = Field(..., description="Chunk text content")
    metadata: DocumentMetadata = Field(..., description="Chunk metadata")

class IngestRequest(BaseModel):
    """Request model for document ingestion"""
    force_reload: bool = Field(
        default=False, 
        description="Force reload all documents even if already ingested"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "force_reload": False
            }
        }

class IngestResponse(BaseModel):
    """Response model for document ingestion"""
    status: str = Field(..., description="Ingestion status")
    documents_processed: int = Field(..., description="Number of documents processed")
    chunks_created: int = Field(..., description="Number of chunks created")
    message: str = Field(..., description="Status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "documents_processed": 3,
                "chunks_created": 45,
                "message": "Successfully ingested 3 documents into vector store"
            }
        }

class SearchResult(BaseModel):
    """A single search result"""
    content: str = Field(..., description="Chunk content")
    source: str = Field(..., description="Source file")
    score: float = Field(..., description="Relevance score (0-1)")
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Async/await is syntactic sugar over Promises...",
                "source": "python_basics.md",
                "score": 0.91,
                "metadata": {"topic": "async", "framework": "JavaScript"}
            }
        }

class SearchRequest(BaseModel):
    """Request model for semantic search"""
    query: str = Field(..., description="Search query (preferably normalized)", min_length=1)
    top_k: int = Field(default=3, description="Number of results to return", ge=1, le=10)
    use_reranking: bool = Field(
        default=True, 
        description="Reranking parameter (currently disabled for demo performance)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "When to use async await in JavaScript",
                "top_k": 3,
                "use_reranking": True
            }
        }

class SearchResponse(BaseModel):
    """Response model for semantic search"""
    query: str = Field(..., description="Original search query")
    results: List[SearchResult] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "When to use async await in JavaScript",
                "results": [
                    {
                        "content": "Async/await is syntactic sugar...",
                        "source": "python_basics.md",
                        "score": 0.91,
                        "metadata": {}
                    }
                ],
                "total_results": 3
            }
        }
