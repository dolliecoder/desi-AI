"""Pydantic models for ask endpoint"""

from pydantic import BaseModel, Field
from typing import List, Optional

class AskRequest(BaseModel):
    """Request model for ask endpoint"""
    query: str = Field(..., description="User's coding question in any language", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Bhai async await kab use karte hai?"
            }
        }

class RetrievedContext(BaseModel):
    """Retrieved context chunk"""
    content: str = Field(..., description="Retrieved content")
    source: str = Field(..., description="Source file")
    score: float = Field(..., description="Relevance score")

class AskResponse(BaseModel):
    """Response model for ask endpoint"""
    query: str = Field(..., description="Original user query")
    normalized_query: str = Field(..., description="Normalized query used for retrieval")
    answer: str = Field(..., description="Generated answer from Gemini")
    context_used: List[RetrievedContext] = Field(..., description="Retrieved context chunks")
    detected_language: str = Field(..., description="Detected language style")
    explanation_style: str = Field(..., description="Detected explanation style")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Bhai async await kab use karte hai?",
                "normalized_query": "When to use async await in JavaScript",
                "answer": "Async/await is used when you need to handle asynchronous operations...",
                "context_used": [
                    {
                        "content": "Async/await is syntactic sugar over Promises...",
                        "source": "python_basics.md",
                        "score": 0.91
                    }
                ],
                "detected_language": "Hinglish",
                "explanation_style": "Beginner"
            }
        }
