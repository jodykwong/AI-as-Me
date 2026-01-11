"""LLM client wrapper."""
from openai import OpenAI
from typing import Optional, List, Dict
import time


class LLMClient:
    """Wrapper for OpenAI-compatible LLM API."""
    
    client: OpenAI
    model: str
    
    def __init__(self, api_key: str, base_url: str, model: str = "deepseek-chat") -> None:
        """Initialize LLM client.
        
        Args:
            api_key: API key
            base_url: API base URL
            model: Model name
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0,
            max_retries=0,  # We handle retries ourselves
        )
        self.model = model
    
    def chat(self, messages: List[Dict[str, str]], max_retries: int = 3) -> Optional[str]:
        """Send chat completion request with retry logic.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_retries: Maximum retry attempts
            
        Returns:
            Response content or None if failed
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                last_error = e
                error_type = type(e).__name__
                
                # Check if error is retryable
                if "timeout" in str(e).lower() or "5" in str(e)[:3]:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        print(f"⚠️  {error_type}, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                
                # Non-retryable error
                print(f"❌ {error_type}: {e}")
                return None
        
        print(f"❌ Failed after {max_retries} attempts: {last_error}")
        return None
