"""Service for generating embeddings using lightweight model"""

from sentence_transformers import SentenceTransformer
from typing import List, Union
from utils.config import settings
import traceback

class EmbeddingService:
    """Service for generating multilingual embeddings"""
    
    def __init__(self):
        """Initialize embedding model"""
        try:
            print(f"Loading embedding model: {settings.embedding_model}")
            self.model = SentenceTransformer(settings.embedding_model)
            dimension = self.model.get_sentence_embedding_dimension()
            print(f"✓ Embedding model loaded (dimension: {dimension})")
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            traceback.print_exc()
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
        
        Returns:
            Embedding vector as list of floats
        """
        try:
            embedding = self.model.encode(text, normalize_embeddings=True)
            return embedding.tolist()
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            traceback.print_exc()
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing)
        
        Args:
            texts: List of input texts
        
        Returns:
            List of embedding vectors
        """
        try:
            if not texts:
                return []
            
            print(f"  Encoding {len(texts)} texts...")
            embeddings = self.model.encode(
                texts, 
                normalize_embeddings=True, 
                show_progress_bar=False,
                batch_size=32  # Process in batches
            )
            print(f"  ✓ Encoding complete")
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            print(f"❌ Error generating embeddings: {e}")
            traceback.print_exc()
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        try:
            return self.model.get_sentence_embedding_dimension()
        except Exception as e:
            print(f"❌ Error getting dimension: {e}")
            return 0

# Singleton instance
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
