"""Service for handling ask queries with RAG pipeline"""

from models.ask import AskResponse, RetrievedContext
from services.normalization_service import get_normalization_service
from services.retrieval_service import get_retrieval_service
from services.gemini_service import get_gemini_service
from prompts.system_prompts import CODESWITCH_SYSTEM_PROMPT

class AskService:
    """Service for RAG-powered question answering"""
    
    def __init__(self):
        """Initialize ask service"""
        print("[ASK] Initializing ask service")
        self.normalization_service = get_normalization_service()
        self.retrieval_service = get_retrieval_service()
        self.gemini_service = get_gemini_service()
    
    async def ask(self, query: str) -> AskResponse:
        """
        Answer a coding question using RAG pipeline
        
        Args:
            query: User's coding question in any language
        
        Returns:
            AskResponse with answer and metadata
        """
        print(f"\n[ASK] ========== Processing query ==========")
        print(f"[ASK] Query: {query}")
        
        try:
            # Step 1: Normalize query
            print("[ASK] Step 1: Normalizing query...")
            normalized = await self.normalization_service.normalize_query(query)
            print(f"[ASK] Normalized: {normalized.normalized_query}")
            print(f"[ASK] Language: {normalized.detected_language}, Style: {normalized.explanation_style}")
            
            # Step 2: Retrieve relevant context
            print("[ASK] Step 2: Retrieving context...")
            search_results = self.retrieval_service.search(
                query=normalized.normalized_query,
                top_k=3,
                use_reranking=False
            )
            print(f"[ASK] Retrieved {len(search_results)} context chunks")
            
            # Step 3: Build context for Gemini
            context_text = self._build_context(search_results)
            print(f"[ASK] Built context: {len(context_text)} characters")
            
            # Step 4: Generate answer with Gemini
            print("[ASK] Step 3: Generating answer with Gemini...")
            answer = await self._generate_answer(
                original_query=query,
                normalized_query=normalized.normalized_query,
                context=context_text,
                language=normalized.detected_language,
                style=normalized.explanation_style
            )
            print(f"[ASK] Answer generated: {len(answer)} characters")
            
            # Build response
            response = AskResponse(
                query=query,
                normalized_query=normalized.normalized_query,
                answer=answer,
                context_used=[
                    RetrievedContext(
                        content=result.content[:200] + "..." if len(result.content) > 200 else result.content,
                        source=result.source,
                        score=result.score
                    )
                    for result in search_results
                ],
                detected_language=normalized.detected_language,
                explanation_style=normalized.explanation_style
            )
            
            print(f"[ASK] ✓ Response complete")
            return response
            
        except Exception as e:
            print(f"[ASK] ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _build_context(self, search_results) -> str:
        """Build context string from search results"""
        if not search_results:
            return "No relevant context found in knowledge base."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"[Context {i} - from {result.source}]")
            context_parts.append(result.content)
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    async def _generate_answer(
        self,
        original_query: str,
        normalized_query: str,
        context: str,
        language: str,
        style: str
    ) -> str:
        """Generate answer using Gemini with context"""
        
        # Build prompt with context
        user_prompt = f"""User Question: {original_query}

Normalized Query: {normalized_query}

Detected Language: {language}
Explanation Style: {style}

Retrieved Context from Knowledge Base:
{context}

Instructions:
1. Answer the user's question using the provided context
2. If the user asked in Hindi/Hinglish, respond in that language style
3. Match the explanation style ({style}):
   - Beginner: Simple, step-by-step explanations with examples
   - Interview: Concise, focused on key concepts and comparisons
   - Advanced: Technical depth, internals, edge cases
4. If context is insufficient, provide a general answer but mention it's not from the knowledge base
5. Include code examples when relevant
6. Be conversational and helpful

Answer:"""
        
        # Generate response
        answer = await self.gemini_service.generate_response(
            system_prompt=CODESWITCH_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.7
        )
        
        return answer.strip()

# Singleton instance
_ask_service = None

def get_ask_service() -> AskService:
    """Get or create ask service instance"""
    global _ask_service
    if _ask_service is None:
        print("[ASK] Creating new ask service")
        _ask_service = AskService()
    return _ask_service
