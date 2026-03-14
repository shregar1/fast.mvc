"""Re-export from fastmvc_core for backward compatibility."""

from fastmvc_core.services.llm.base import (
    ILLMService,
    OpenAILLMService,
    AnthropicLLMService,
    OllamaLLMService,
    build_llm_service,
)

__all__ = [
    "ILLMService",
    "OpenAILLMService",
    "AnthropicLLMService",
    "OllamaLLMService",
    "build_llm_service",
]
