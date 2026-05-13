"""Service for ChromaDB vector store operations"""

import os
import sys

# Completely disable ChromaDB telemetry
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Mock posthog to prevent the "capture() takes 1 positional argument but 3 were given" error
class DummyPosthog:
    def capture(self, *args, **kwargs): pass
sys.modules['posthog'] = DummyPosthog()

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from utils.config import settings
from models.rag import DocumentChunk, SearchResult
from services.embedding_service import get_embedding_service
import traceback

class VectorStoreService:
    """Service for managing ChromaDB vector store"""
    
    COLLECTION_NAME = "codeswitch_knowledge"
    
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Ensure persist directory exists
            os.makedirs(settings.chroma_persist_dir, exist_ok=True)
            
            # Initialize ChromaDB client with persistent storage and telemetry disabled
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get embedding service
            self.embedding_service = get_embedding_service()
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"description": "CodeSwitch AI knowledge base"}
            )
            
            print(f"✓ ChromaDB initialized with {self.collection.count()} documents")
        except Exception as e:
            print(f"❌ Error initializing ChromaDB: {e}")
            traceback.print_exc()
            raise
    
    def add_documents(self, chunks: List[DocumentChunk]) -> int:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of document chunks with content and metadata
        
        Returns:
            Number of chunks added
        """
        if not chunks:
            print("⚠ No chunks to add")
            return 0
        
        try:
            # Extract content and metadata
            documents = [chunk.content for chunk in chunks]
            metadatas = [chunk.metadata.model_dump() for chunk in chunks]
            
            print(f"Generating embeddings for {len(documents)} chunks...")
            
            # Generate embeddings with error handling
            try:
                embeddings = self.embedding_service.generate_embeddings(documents)
                print(f"✓ Embeddings generated")
            except Exception as e:
                print(f"❌ Error generating embeddings: {e}")
                traceback.print_exc()
                raise
            
            # Generate IDs
            ids = [f"doc_{i}_{chunk.metadata.source}_{chunk.metadata.chunk_index}" 
                   for i, chunk in enumerate(chunks)]
            
            # Add to collection
            print(f"Adding {len(chunks)} chunks to vector store...")
            try:
                self.collection.add(
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"✓ Added to vector store")
            except Exception as e:
                print(f"❌ Error adding to ChromaDB: {e}")
                traceback.print_exc()
                raise
            
            total_docs = self.collection.count()
            print(f"Total documents in store: {total_docs}")
            
            return len(chunks)
            
        except Exception as e:
            print(f"❌ Error in add_documents: {e}")
            traceback.print_exc()
            raise
    
    def search(
        self, 
        query: str, 
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Semantic search in vector store
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of search results with content, metadata, and scores
        """
        try:
            print(f"Generating query embedding...")
            # Generate query embedding
            query_embedding = self.embedding_service.generate_embedding(query)
            
            print(f"Searching in vector store...")
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self.collection.count())
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0.0,
                        'id': results['ids'][0][i] if results['ids'] else ''
                    })
            
            print(f"✓ Found {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            print(f"❌ Error in search: {e}")
            traceback.print_exc()
            raise
    
    def clear_collection(self):
        """Clear all documents from collection"""
        try:
            print("Clearing vector store...")
            self.client.delete_collection(self.COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"description": "CodeSwitch AI knowledge base"}
            )
            print("✓ Vector store cleared")
        except Exception as e:
            print(f"❌ Error clearing collection: {e}")
            traceback.print_exc()
            raise
    
    def get_count(self) -> int:
        """Get number of documents in collection"""
        try:
            return self.collection.count()
        except Exception as e:
            print(f"❌ Error getting count: {e}")
            traceback.print_exc()
            return 0

# Singleton instance
_vectorstore_service = None

def get_vectorstore_service() -> VectorStoreService:
    """Get or create vector store service instance"""
    global _vectorstore_service
    if _vectorstore_service is None:
        _vectorstore_service = VectorStoreService()
    return _vectorstore_service
