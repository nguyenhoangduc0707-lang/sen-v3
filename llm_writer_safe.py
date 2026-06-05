"""
Safe LLM Writer với Circuit Breaker protection
"""
import asyncio
import logging
from typing import Optional, Dict, Any
from circuit_breaker import circuit_registry

logger = logging.getLogger(__name__)


class SafeLLMWriter:
    def __init__(self):
        self.circuit_breaker = circuit_registry.get("gemini_api")
        self.fallback_enabled = True
    
    async def generate_content(self, prompt: str, max_retries: int = 2) -> Optional[str]:
        """Generate content with circuit breaker protection"""
        
        for attempt in range(max_retries):
            try:
                # Try Gemini first
                result = await self.circuit_breaker.call(self._call_gemini, prompt)
                if result:
                    return result
                
                # Fallback to GPT if available
                if self.fallback_enabled:
                    result = await self._call_gpt(prompt)
                    if result:
                        return result
                        
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        logger.error("All attempts failed, circuit may be OPEN")
        return None
    
    async def _call_gemini(self, prompt: str) -> Optional[str]:
        """Call Gemini API"""
        try:
            # Import và gọi Gemini API
            import google.generativeai as genai
            import os
            
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = await asyncio.to_thread(model.generate_content, prompt)
            
            return response.text
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise e
    
    async def _call_gpt(self, prompt: str) -> Optional[str]:
        """Fallback to GPT-4"""
        try:
            # Import và gọi OpenAI API
            from openai import AsyncOpenAI
            import os
            
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"GPT error: {e}")
            return None
    
    async def get_circuit_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        return self.circuit_breaker.get_state()


# Singleton instance
safe_llm_writer = SafeLLMWriter()
