"""In-memory document store for uploaded PDFs"""

from typing import Dict, List, Any
from collections import Counter
import re

class PDFDocumentStore:
    """Store for uploaded PDF documents"""
    
    def __init__(self):
        """Initialize document store"""
        self.documents = []  # List of {content, source, chunk_index}
        self.current_pdf = None  # Current PDF filename
        print("[PDF_STORE] Initialized")
    
    def clear(self):
        """Clear all documents"""
        print("[PDF_STORE] Clearing all documents")
        self.documents = []
        self.current_pdf = None
    
    def add_pdf_chunks(self, chunks: List[str], filename: str):
        """
        Add PDF chunks to store
        
        Args:
            chunks: List of text chunks
            filename: PDF filename
        """
        print(f"[PDF_STORE] Adding {len(chunks)} chunks from {filename}")
        
        # Clear previous documents
        self.clear()
        
        # Add new chunks
        for i, chunk in enumerate(chunks):
            self.documents.append({
                'content': chunk,
                'source': filename,
                'chunk_index': i
            })
        
        self.current_pdf = filename
        print(f"[PDF_STORE] ✓ Added {len(chunks)} chunks")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search documents using keyword matching
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of matching documents with scores
        """
        print(f"[PDF_STORE] Searching for: '{query}' (top_k={top_k})")
        
        if not self.documents:
            print("[PDF_STORE] No documents in store")
            return []
        
        # Extract query keywords
        query_keywords = self._extract_keywords(query)
        print(f"[PDF_STORE] Query keywords: {query_keywords[:10]}")
        
        if not query_keywords:
            # If no keywords, return first few chunks
            print("[PDF_STORE] No keywords, returning first chunks")
            return [
                {
                    'content': doc['content'],
                    'source': doc['source'],
                    'score': 1.0,
                    'metadata': {}
                }
                for doc in self.documents[:top_k]
            ]
        
        # Score documents
        scored_docs = []
        for doc in self.documents:
            doc_keywords = self._extract_keywords(doc['content'])
            matches = sum(1 for kw in query_keywords if kw in doc_keywords)
            score = matches / len(query_keywords) if query_keywords else 0.0
            
            if score > 0:
                scored_docs.append({
                    'content': doc['content'],
                    'source': doc['source'],
                    'score': score,
                    'metadata': {}
                })
        
        # Sort by score
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        
        results = scored_docs[:top_k]
        print(f"[PDF_STORE] ✓ Returning {len(results)} results")
        
        return results
    
    def get_all_content(self) -> str:
        """Get all document content as single string"""
        if not self.documents:
            return ""
        
        return "\n\n".join(doc['content'] for doc in self.documents)
    
    def has_documents(self) -> bool:
        """Check if store has documents"""
        return len(self.documents) > 0

# Singleton instance
_pdf_document_store = None

def get_pdf_document_store() -> PDFDocumentStore:
    """Get or create PDF document store instance"""
    global _pdf_document_store
    if _pdf_document_store is None:
        print("[PDF_STORE] Creating new document store")
        _pdf_document_store = PDFDocumentStore()
    return _pdf_document_store
