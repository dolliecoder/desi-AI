"""API routes for query normalization"""

from fastapi import APIRouter, HTTPException, status
from models.normalization import NormalizationRequest, NormalizationResponse
from services.normalization_service import get_normalization_service
import traceback

router = APIRouter(prefix="/normalize", tags=["Normalization"])

@router.post(
    "",
    response_model=NormalizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Normalize multilingual coding query",
    description="""
    Normalize a multilingual coding query into clean technical English.
    
    Supports:
    - English, Hindi, Hinglish, and mixed queries
    - Automatic language detection
    - Explanation style detection (Beginner/Interview/Advanced)
    
    The normalized query is optimized for semantic search in a coding knowledge base.
    """
)
async def normalize_query(request: NormalizationRequest):
    """
    Normalize a multilingual coding query
    
    Args:
        request: NormalizationRequest with raw query
    
    Returns:
        NormalizationResponse with normalized query and metadata
    
    Raises:
        HTTPException: If normalization fails
    """
    try:
        print(f"\n{'='*60}")
        print(f"Normalization Request: {request.query}")
        print(f"{'='*60}")
        
        # Get normalization service
        service = get_normalization_service()
        
        # Normalize the query
        result = await service.normalize_query(request.query)
        
        print(f"✓ Normalization successful")
        print(f"  Original: {result.original_query}")
        print(f"  Normalized: {result.normalized_query}")
        print(f"  Language: {result.detected_language}")
        print(f"  Style: {result.explanation_style}")
        print(f"{'='*60}\n")
        
        return result
        
    except ValueError as e:
        # Handle validation or parsing errors
        print(f"❌ Validation error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to normalize query: {str(e)}"
        )
    except Exception as e:
        # Handle unexpected errors
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
