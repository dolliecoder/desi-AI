from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns service status and timestamp
    """
    return {
        "status": "healthy",
        "service": "CodeSwitch AI",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat()
    }
