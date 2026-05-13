"""OpenAI-compatible API service for LLM operations (async)"""

import aiohttp
import json
from typing import Dict, Any, Optional
from utils.config import settings
import traceback

class GeminiService:
    """Async service for OpenAI-compatible LLM API"""
    
    def __init__(self):
        """Initialize OpenAI-compatible API service"""
        self.api_key = settings.openai_api_key
        self.raw_base_url = settings.openai_base_url
        self.model = settings.openai_model
        self._session: Optional[aiohttp.ClientSession] = None
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured in environment")
        if not self.raw_base_url:
            raise ValueError("OPENAI_BASE_URL not configured in environment")
        if not self.model:
            raise ValueError("OPENAI_MODEL not configured in environment")
        
        # If base_url is a full endpoint URL (ends with /chat/completions or similar),
        # use it directly. Otherwise append /chat/completions
        self.base_url = self.raw_base_url.rstrip("/")
        self._has_full_path = any(self.base_url.endswith(p) for p in [
            "/chat/completions", "/completions", "/generate", "/v1"
        ])
        
        print(f"✓ OpenAI API initialized: model={self.model}")
        print(f"   Base URL: {self.raw_base_url}")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create persistent aiohttp session"""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=10, force_close=False)
            self._session = aiohttp.ClientSession(
                connector=connector,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self._session
    
    async def close(self):
        """Close the persistent session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    def _build_chat_url(self) -> str:
        """Build the chat completions API URL"""
        url = self.base_url
        # If base_url already contains the full chat completions path, use as-is
        if url.endswith("/chat/completions") or url.endswith("/v1"):
            if url.endswith("/v1"):
                url = url + "/chat/completions"
            return url
        # Otherwise assume it's a base API URL and append chat/completions
        return url.rstrip("/") + "/chat/completions"
    
    def _build_messages(self, system_prompt: str, user_prompt: str) -> list:
        """Build messages array for chat completion"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return messages
    
    async def generate_response(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate response from OpenAI-compatible API (async, non-streaming)
        
        Args:
            system_prompt: System instructions
            user_prompt: User query
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Max tokens to generate
        
        Returns:
            Generated text response
        """
        url = self._build_chat_url()
        messages = self._build_messages(system_prompt, user_prompt)
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        print(f"\n[LLM] Sending request...")
        print(f"   URL: {url}")
        print(f"   Model: {self.model}")
        print(f"   Messages: {len(messages)} (system={bool(system_prompt)}, user={len(user_prompt)} chars)")
        
        try:
            session = await self._get_session()
            
            async with session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                print(f"   Response status: {resp.status}")
                
                if resp.status != 200:
                    error_text = await resp.text()
                    print(f"   Error body (first 300 chars): {error_text[:300]}")
                    raise Exception(
                        f"API error {resp.status}: "
                        f"{error_text[:500]}"
                    )
                
                result = await resp.json()
                
                if "choices" not in result or not result["choices"]:
                    raise Exception(f"Unexpected API response format: {json.dumps(result)[:300]}")
                
                content = result["choices"][0]["message"].get("content")
                # Some models return content in "reasoning" field instead of "content"
                if content is None:
                    content = result["choices"][0]["message"].get("reasoning", "")
                    print(f"⚠ Content was null, using reasoning field ({len(content)} chars)")
                if not content:
                    raise Exception(f"API returned empty response. Full: {json.dumps(result)[:500]}")
                print(f"✓ Received response ({len(content)} chars)")
                return content
                
        except aiohttp.ClientError as e:
            print(f"❌ Network error: {e}")
            traceback.print_exc()
            raise
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            traceback.print_exc()
            raise
    
    async def generate_json_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3
    ) -> Dict[Any, Any]:
        """
        Generate JSON response from OpenAI-compatible API (async)
        
        Args:
            system_prompt: System instructions
            user_prompt: User query
            temperature: Sampling temperature
        
        Returns:
            Parsed JSON response
        
        Raises:
            ValueError: If response is not valid JSON
        """
        try:
            response_text = await self.generate_response(
                system_prompt, 
                user_prompt, 
                temperature
            )
            
            # Extract JSON from response (handle markdown code blocks)
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            print(f"Parsing JSON response...")
            parsed = json.loads(response_text)
            print(f"✓ JSON parsed successfully")
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print(f"Response text: {response_text[:200]}...")
            traceback.print_exc()
            raise ValueError(f"Failed to parse JSON response: {e}")
        except Exception as e:
            print(f"❌ Error in generate_json_response: {e}")
            traceback.print_exc()
            raise

# Singleton instance
_gemini_service = None

def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
