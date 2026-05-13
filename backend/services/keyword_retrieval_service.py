"""Lightweight keyword-based retrieval service for demo stability"""

import re
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

class KeywordRetrievalService:
    """Simple keyword-based document retrieval"""
    
    def __init__(self):
        """Initialize keyword retrieval service"""
        self.documents = []
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        print(f"[KEYWORD] Initialized. Data dir: {self.data_dir}")
    
    def load_documents(self) -> int:
        """
        Load markdown documents from data directory
        
        Returns:
            Number of documents loaded
        """
        print(f"[KEYWORD] Starting document load...")
        self.documents = []
        
        # Check if data directory exists
        if not self.data_dir.exists():
            print(f"[KEYWORD] ERROR: Data directory not found: {self.data_dir}")
            return 0
        
        # Find markdown files
        try:
            md_files = list(self.data_dir.glob('*.md'))
            print(f"[KEYWORD] Found {len(md_files)} markdown files")
        except Exception as e:
            print(f"[KEYWORD] ERROR: Failed to list files: {e}")
            return 0
        
        if not md_files:
            print(f"[KEYWORD] WARNING: No markdown files in {self.data_dir}")
            return 0
        
        # Load each file
        for md_file in md_files:
            print(f"[KEYWORD] Loading: {md_file.name}")
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"[KEYWORD]   Read {len(content)} characters")
                
                # Simple chunking - split by double newline or every 1000 chars
                chunks = self._simple_chunk(content)
                print(f"[KEYWORD]   Created {len(chunks)} chunks")
                
                # Add chunks to documents
                for i, chunk in enumerate(chunks):
                    self.documents.append({
                        'content': chunk,
                        'source': md_file.name,
                        'chunk_index': i
                    })
                
            except Exception as e:
                print(f"[KEYWORD] ERROR loading {md_file.name}: {e}")
                continue
        
        print(f"[KEYWORD] ✓ Loaded {len(self.documents)} total chunks")
        return len(self.documents)
    
    def _simple_chunk(self, text: str, max_size: int = 1000) -> List[str]:
        """Simple text chunking without overlap"""
        print(f"[KEYWORD]   Chunking text of length {len(text)}")
        
        # Remove frontmatter if present
        if text.startswith('---'):
            parts = text.split('---', 2)
            if len(parts) >= 3:
                text = parts[2].strip()
        
        # If text is small enough, return as single chunk
        if len(text) <= max_size:
            return [text]
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) <= max_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Convert to lowercase and extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Simple stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Filter and return
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search documents using keyword matching
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of search results with content, source, and score
        """
        print(f"[KEYWORD] Search called with query: '{query}', top_k: {top_k}")
        
        # Load documents if not loaded
        if not self.documents:
            print(f"[KEYWORD] No documents loaded, loading now...")
            count = self.load_documents()
            if count == 0:
                print(f"[KEYWORD] No documents available after load")
                return []
        
        print(f"[KEYWORD] Searching {len(self.documents)} documents")
        
        # Extract query keywords
        query_keywords = self._extract_keywords(query)
        print(f"[KEYWORD] Query keywords: {query_keywords[:10]}")  # Show first 10
        
        if not query_keywords:
            print(f"[KEYWORD] No keywords extracted from query")
            return []
        
        # Score documents
        scored_docs = []
        for idx, doc in enumerate(self.documents):
            doc_keywords = self._extract_keywords(doc['content'])
            
            # Count matches
            matches = sum(1 for kw in query_keywords if kw in doc_keywords)
            score = matches / len(query_keywords) if query_keywords else 0.0
            
            if score > 0:
                scored_docs.append({
                    'content': doc['content'],
                    'source': doc['source'],
                    'score': score,
                    'metadata': {}
                })
        
        print(f"[KEYWORD] Found {len(scored_docs)} documents with matches")
        
        # Sort by score
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top K
        results = scored_docs[:top_k]
        print(f"[KEYWORD] Returning {len(results)} results")
        
        return results

# Singleton instance
_keyword_retrieval_service = None

def get_keyword_retrieval_service() -> KeywordRetrievalService:
    """Get or create keyword retrieval service instance"""
    global _keyword_retrieval_service
    if _keyword_retrieval_service is None:
        print("[KEYWORD] Creating new service instance")
        _keyword_retrieval_service = KeywordRetrievalService()
    return _keyword_retrieval_service
