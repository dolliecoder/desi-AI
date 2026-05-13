"""Service for reranking search results using BAAI/bge-reranker-base"""

from sentence_transformers import CrossEncoder
from typing import List, Dict, Any

class RerankerService:
    """Service for reranking search results"""
    
    RERANKER_MODEL = "BAAI/bge-reranker-base"
    
    def __init__(self):
        """Initialize reranker model"""
        print(f"Loading reranker model: {self.RERANKER_MODEL}")
        self.model = CrossEncoder(self.RERANKER_MODEL)
        print("✓ Reranker model loaded successfully")
    
    def rerank(
        self, 
        query: str, 
        results: List[Dict[str, Any]], 
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Rerank search results based on query relevance
        
        Args:
            query: Search query
            results: List of search results from vector store
            top_k: Number of top results to return after reranking
        
        Returns:
            Reranked and filtered results
        """
        if not results:
            return []
        
        # Prepare query-document pairs
        pairs = [[query, result['content']] for result in results]
        
        # Get reranking scores
        scores = self.model.predict(pairs)
        
        # Add scores to results
        for i, result in enumerate(results):
            result['rerank_score'] = float(scores[i])
        
        # Sort by rerank score (descending)
        reranked = sorted(results, key=lambda x: x['rerank_score'], reverse=True)
        
        # Return top_k results
        return reranked[:top_k]

# Singleton instance
_reranker_service = None

def get_reranker_service() -> RerankerService:
    """Get or create reranker service instance"""
    global _reranker_service
    if _reranker_service is None:
        _reranker_service = RerankerService()
    return _reranker_service
