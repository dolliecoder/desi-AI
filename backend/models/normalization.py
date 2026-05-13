from pydantic import BaseModel, Field
from typing import Literal

class NormalizationRequest(BaseModel):
    """Request model for query normalization"""
    query: str = Field(..., description="Raw multilingual coding query", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Bhai async await kab use karte hai?"
            }
        }

class NormalizationResponse(BaseModel):
    """Response model for normalized query"""
    original_query: str = Field(..., description="Original user query")
    normalized_query: str = Field(..., description="Clean technical English query for retrieval")
    detected_language: str = Field(..., description="Detected language style (English/Hindi/Hinglish/Mixed)")
    explanation_style: Literal["Beginner", "Interview", "Advanced"] = Field(
        ..., 
        description="Detected explanation complexity level"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_query": "Bhai async await kab use karte hai?",
                "normalized_query": "When to use async await in JavaScript",
                "detected_language": "Hinglish",
                "explanation_style": "Beginner"
            }
        }
