"""Service for semantic retrieval using lightweight keyword matching"""

from typing import List
from models.rag import SearchResult
from services.keyword_retrieval_service import get_keyword_retrieval_service

class RetrievalService:
    """Service for keyword-based search and retrieval"""
    
    def __init__(self):
        """Initialize retrieval service"""
        print("[RETRIEVAL] Initializing retrieval service")
        self.keyword_service = get_keyword_retrieval_service()
    
    def search(
        self, 
        query: str, 
        top_k: int = 3,
        use_reranking: bool = True
    ) -> List[SearchResult]:
        """
        Perform keyword-based search
        
        Args:
            query: Search query (preferably normalized)
            top_k: Number of final results to return
            use_reranking: Ignored (no reranking in keyword search)
        
        Returns:
            List of search results ordered by relevance
        """
        print(f"[RETRIEVAL] Search called: query='{query}', top_k={top_k}")
        
        try:
            # Perform keyword search
            print("[RETRIEVAL] Calling keyword service search...")
            raw_results = self.keyword_service.search(query, top_k=top_k)
            print(f"[RETRIEVAL] Got {len(raw_results)} raw results")
            
            if not raw_results:
                print("[RETRIEVAL] No results found")
                return []
            
            # Convert to SearchResult models
            search_results = []
            for idx, result in enumerate(raw_results):
                print(f"[RETRIEVAL] Processing result {idx+1}: source={result.get('source')}, score={result.get('score')}")
                search_results.append(SearchResult(
                    content=result['content'],
                    source=result.get('source', 'unknown'),
                    score=round(result['score'], 3),
                    metadata=result.get('metadata', {})
                ))
            
            print(f"[RETRIEVAL] ✓ Returning {len(search_results)} results")
            return search_results
            
        except Exception as e:
            print(f"[RETRIEVAL] ERROR: {e}")
            import traceback
            traceback.print_exc()
            return []

# Singleton instance
_retrieval_service = None

def get_retrieval_service() -> RetrievalService:
    """Get or create retrieval service instance"""
    global _retrieval_service
    if _retrieval_service is None:
        print("[RETRIEVAL] Creating new retrieval service")
        _retrieval_service = RetrievalService()
    return _retrieval_service
