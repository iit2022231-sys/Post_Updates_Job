"""
Free_API_Load_balancer: Load-balanced LLM provider module
Simply import and use - everything is pre-configured
"""

from .model_provider import ProviderRegistry, LLMProvider, GeminiLLMProvider, GroqLLMProvider
from .load_balancer import LoadBalancer

# Auto-register all providers on import
ProviderRegistry.register("Gemini", GeminiLLMProvider)
ProviderRegistry.register("Groq", GroqLLMProvider)

# Create singleton instance (lazy-loaded)
_lb_instance = None

def get_load_balancer():
    """Get or create the LoadBalancer singleton instance"""
    global _lb_instance
    if _lb_instance is None:
        _lb_instance = LoadBalancer()
    return _lb_instance

def generate(prompt: str, max_output_tokens: int = 300) -> str:
    """
    Simple API: Just give prompt, get response back!
    Handles load balancing and provider selection automatically.
    
    Args:
        prompt: The input prompt to send to the LLM
        max_output_tokens: Maximum tokens in the response (default: 300)
    
    Returns:
        Generated response text from the LLM
    """
    lb = get_load_balancer()
    provider = lb.start(text=prompt, max_output_tokens=max_output_tokens)
    return provider.generate_response(prompt=prompt)

# Public exports
__all__ = [
    'LoadBalancer',
    'ProviderRegistry',
    'LLMProvider',
    'GeminiLLMProvider',
    'GroqLLMProvider',
    'get_load_balancer',
    'generate',
]