"""Pydantic models for PDF operations"""

from pydantic import BaseModel, Field
from typing import List

class PDFUploadResponse(BaseModel):
    """Response model for PDF upload"""
    filename: str = Field(..., description="Uploaded filename")
    num_chunks: int = Field(..., description="Number of text chunks created")
    total_chars: int = Field(..., description="Total characters extracted")
    message: str = Field(..., description="Status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "document.pdf",
                "num_chunks": 5,
                "total_chars": 4523,
                "message": "PDF uploaded and processed successfully"
            }
        }

class PDFAskRequest(BaseModel):
    """Request model for asking questions about uploaded PDF"""
    query: str = Field(..., description="Question about the PDF content", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Is document ke baare mein batao"
            }
        }

class PDFAskResponse(BaseModel):
    """Response model for PDF-based questions"""
    query: str = Field(..., description="Original user query")
    answer: str = Field(..., description="AI-generated answer based on PDF")
    source: str = Field(..., description="Source PDF filename")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Is document ke baare mein batao",
                "answer": "Yeh document...",
                "source": "document.pdf"
            }
        }
