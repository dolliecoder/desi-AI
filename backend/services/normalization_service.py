"""Service for multilingual query normalization"""

from models.normalization import NormalizationResponse
from prompts.normalization_prompts import (
    NORMALIZATION_SYSTEM_PROMPT,
    get_normalization_prompt
)
from services.gemini_service import get_gemini_service
from typing import Dict, Any

class NormalizationService:
    """Service for normalizing multilingual coding queries"""
    
    def __init__(self):
        """Initialize normalization service"""
        self.gemini_service = get_gemini_service()
    
    async def normalize_query(self, query: str) -> NormalizationResponse:
        """
        Normalize a multilingual coding query
        
        Args:
            query: Raw multilingual query from user
        
        Returns:
            NormalizationResponse with normalized query and metadata
        
        Raises:
            ValueError: If normalization fails or response is invalid
        """
        try:
            # Generate normalization prompt
            user_prompt = get_normalization_prompt(query)
            
            # Get normalized response from Gemini
            response_json = await self.gemini_service.generate_json_response(
                system_prompt=NORMALIZATION_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=0.3  # Low temperature for consistent normalization
            )
            
            # Validate response structure
            required_fields = ["normalized_query", "detected_language", "explanation_style"]
            for field in required_fields:
                if field not in response_json:
                    raise ValueError(f"Missing required field in response: {field}")
            
            # Create response model
            return NormalizationResponse(
                original_query=query,
                normalized_query=response_json["normalized_query"],
                detected_language=response_json["detected_language"],
                explanation_style=response_json["explanation_style"]
            )
        except Exception as e:
            print(f"⚠ Normalization failed, using fallback: {e}")
            import traceback
            traceback.print_exc()
            return NormalizationResponse(
                original_query=query,
                normalized_query=query,
                detected_language="Unknown",
                explanation_style="Beginner"
            )

# Singleton instance
_normalization_service = None

def get_normalization_service() -> NormalizationService:
    """Get or create normalization service instance"""
    global _normalization_service
    if _normalization_service is None:
        _normalization_service = NormalizationService()
    return _normalization_service
