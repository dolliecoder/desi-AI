"""API routes for RAG operations (ingestion and retrieval)"""

from fastapi import APIRouter, HTTPException, status
from models.rag import (
    IngestRequest, IngestResponse,
    SearchRequest, SearchResponse
)
from services.ingestion_service import get_ingestion_service
from services.retrieval_service import get_retrieval_service
import asyncio

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post(
    "/ingest",
    response_model=IngestResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest documents into memory"
)
async def ingest_documents(request: IngestRequest):
    """Ingest documents into memory"""
    print(f"\n[RAG/INGEST] Endpoint called with force_reload={request.force_reload}")
    
    try:
        service = get_ingestion_service()
        
        # Run with timeout
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(service.ingest_documents, request.force_reload),
                timeout=10.0
            )
        except asyncio.TimeoutError:
            print("[RAG/INGEST] ERROR: Timeout")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Ingestion timed out"
            )
        
        print(f"[RAG/INGEST] ✓ Success")
        return IngestResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[RAG/INGEST] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}"
        )

@router.post(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Keyword search in knowledge base"
)
async def search_knowledge_base(request: SearchRequest):
    """Search knowledge base using keyword retrieval"""
    print(f"\n[RAG/SEARCH] Endpoint called: query='{request.query}'")
    
    try:
        service = get_retrieval_service()
        
        # Run with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.to_thread(
                    service.search,
                    request.query,
                    request.top_k,
                    request.use_reranking
                ),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            print("[RAG/SEARCH] ERROR: Timeout")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Search timed out"
            )
        
        print(f"[RAG/SEARCH] ✓ Success: {len(results)} results")
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_results=len(results)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[RAG/SEARCH] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )
