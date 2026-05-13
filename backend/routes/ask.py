"""API route for ask endpoint - RAG-powered question answering"""

from fastapi import APIRouter, HTTPException, status
from models.ask import AskRequest, AskResponse
from services.ask_service import get_ask_service
import asyncio

router = APIRouter(prefix="/ask", tags=["Ask"])

@router.post(
    "",
    response_model=AskResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a coding question"
)
async def ask_question(request: AskRequest):
    """Ask a coding question and get an AI-powered answer"""
    print(f"\n[ASK/ENDPOINT] Called with query: '{request.query}'")
    
    try:
        service = get_ask_service()
        
        # Run with timeout
        try:
            result = await asyncio.wait_for(
                service.ask(request.query),
                timeout=90.0  # 90 second timeout for full pipeline
            )
        except asyncio.TimeoutError:
            print("[ASK/ENDPOINT] ERROR: Timeout")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Request timed out after 90 seconds"
            )
        
        print(f"[ASK/ENDPOINT] ✓ Success")
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        print(f"[ASK/ENDPOINT] Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to process query: {str(e)}"
        )
    except Exception as e:
        print(f"[ASK/ENDPOINT] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
