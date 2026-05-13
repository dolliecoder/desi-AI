"""Service for PDF processing and text extraction"""

import PyPDF2
from pathlib import Path
from typing import Dict, Any, List
import io

class PDFService:
    """Service for handling PDF uploads and text extraction"""
    
    def __init__(self):
        """Initialize PDF service"""
        self.upload_dir = Path(__file__).parent.parent / "uploads"
        self.upload_dir.mkdir(exist_ok=True)
        print(f"[PDF] Initialized. Upload dir: {self.upload_dir}")
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF bytes
        
        Args:
            pdf_content: PDF file content as bytes
        
        Returns:
            Extracted text from PDF
        """
        print(f"[PDF] Extracting text from PDF ({len(pdf_content)} bytes)")
        
        try:
            # Create PDF reader from bytes
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_parts = []
            num_pages = len(pdf_reader.pages)
            print(f"[PDF] PDF has {num_pages} pages")
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():
                    text_parts.append(text)
                print(f"[PDF] Extracted page {page_num + 1}/{num_pages}")
            
            full_text = "\n\n".join(text_parts)
            print(f"[PDF] ✓ Extracted {len(full_text)} characters total")
            
            return full_text
            
        except Exception as e:
            print(f"[PDF] ERROR extracting text: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Split text into chunks for processing
        
        Args:
            text: Full text to chunk
            chunk_size: Maximum size of each chunk
        
        Returns:
            List of text chunks
        """
        print(f"[PDF] Chunking text ({len(text)} chars) into {chunk_size} char chunks")
        
        if len(text) <= chunk_size:
            return [text]
        
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) <= chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        print(f"[PDF] ✓ Created {len(chunks)} chunks")
        return chunks if chunks else [text]
    
    def process_pdf(self, pdf_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Process uploaded PDF: extract text and chunk it
        
        Args:
            pdf_content: PDF file content
            filename: Original filename
        
        Returns:
            Dictionary with extracted text and chunks
        """
        print(f"[PDF] Processing PDF: {filename}")
        
        try:
            # Extract text
            text = self.extract_text_from_pdf(pdf_content)
            
            if not text.strip():
                raise ValueError("No text could be extracted from PDF")
            
            # Chunk text
            chunks = self.chunk_text(text)
            
            result = {
                'filename': filename,
                'text': text,
                'chunks': chunks,
                'num_chunks': len(chunks),
                'total_chars': len(text)
            }
            
            print(f"[PDF] ✓ Processed {filename}: {len(chunks)} chunks, {len(text)} chars")
            return result
            
        except Exception as e:
            print(f"[PDF] ERROR processing {filename}: {e}")
            raise

# Singleton instance
_pdf_service = None

def get_pdf_service() -> PDFService:
    """Get or create PDF service instance"""
    global _pdf_service
    if _pdf_service is None:
        print("[PDF] Creating new PDF service")
        _pdf_service = PDFService()
    return _pdf_service
