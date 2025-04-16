"""
Core functionality for the LlamaSearch ExperimentalAgents: Product Growth system.

This package contains foundational components like embedding generators,
vector stores, and multi-LLM routing.
"""

from .llm_router import (
    LLMProvider,
    get_available_models,
    get_model_for_task
)

from .llm_client import (
    LLMMessage,
    LLMFunction,
    LLMResponse,
    create_client
)

from .llm import (
    complete_prompt,
    chat_completion,
    analyze_text,
    generate_strategies
)

__all__ = [
    # LLM Router
    "LLMProvider",
    "get_available_models",
    "get_model_for_task",
    
    # LLM Client
    "LLMMessage",
    "LLMFunction", 
    "LLMResponse",
    "create_client",
    
    # High-level LLM utilities
    "complete_prompt",
    "chat_completion",
    "analyze_text",
    "generate_strategies"
] 