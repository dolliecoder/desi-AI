"""Service for ingesting documents (lightweight keyword-based)"""

from typing import Dict, Any
from services.keyword_retrieval_service import get_keyword_retrieval_service

class IngestionService:
    """Service for document ingestion"""
    
    def __init__(self):
        """Initialize ingestion service"""
        print("[INGEST] Initializing ingestion service")
        self.keyword_service = get_keyword_retrieval_service()
    
    def ingest_documents(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Ingest all markdown documents from data directory
        
        Args:
            force_reload: Reload documents even if already loaded
        
        Returns:
            Dictionary with ingestion statistics
        """
        print(f"[INGEST] Starting ingestion (force_reload={force_reload})")
        
        try:
            # Load documents
            print("[INGEST] Calling keyword service load_documents...")
            num_chunks = self.keyword_service.load_documents()
            print(f"[INGEST] Load completed. Chunks: {num_chunks}")
            
            if num_chunks == 0:
                print("[INGEST] WARNING: No documents loaded")
                return {
                    'status': 'warning',
                    'documents_processed': 0,
                    'chunks_created': 0,
                    'message': 'No markdown files found in data directory'
                }
            
            # Count unique sources
            sources = set(doc['source'] for doc in self.keyword_service.documents)
            print(f"[INGEST] Unique sources: {len(sources)}")
            
            result = {
                'status': 'success',
                'documents_processed': len(sources),
                'chunks_created': num_chunks,
                'message': f'Successfully ingested {len(sources)} documents ({num_chunks} chunks)'
            }
            
            print(f"[INGEST] ✓ Ingestion complete: {result}")
            return result
            
        except Exception as e:
            print(f"[INGEST] ERROR: {e}")
            import traceback
            traceback.print_exc()
            return {
                'status': 'error',
                'documents_processed': 0,
                'chunks_created': 0,
                'message': f'Ingestion failed: {str(e)}'
            }

# Singleton instance
_ingestion_service = None

def get_ingestion_service() -> IngestionService:
    """Get or create ingestion service instance"""
    global _ingestion_service
    if _ingestion_service is None:
        print("[INGEST] Creating new ingestion service")
        _ingestion_service = IngestionService()
    return _ingestion_service
