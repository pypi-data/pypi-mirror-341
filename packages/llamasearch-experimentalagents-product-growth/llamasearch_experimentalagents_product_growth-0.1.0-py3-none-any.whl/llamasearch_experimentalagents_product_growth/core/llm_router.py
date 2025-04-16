"""
LLM Router for LlamaSearch ExperimentalAgents: Product Growth.

This module provides functionality to route requests between different 
LLM providers (OpenAI, Anthropic, local models) based on configuration, 
availability, and optimization criteria.
"""

import os
import logging
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class LLMModel(BaseModel):
    """Model representing an LLM model."""
    
    name: str
    provider: LLMProvider
    context_size: int = 8192
    available: bool = True
    hardware: Optional[str] = None
    cost_per_1k_tokens: Optional[float] = None
    input_cost_per_1k_tokens: Optional[float] = None
    output_cost_per_1k_tokens: Optional[float] = None
    capabilities: List[str] = []
    metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary suitable for display."""
        return {
            "name": self.name,
            "provider": self.provider,
            "context_size": self.context_size,
            "available": self.available,
            "hardware": self.hardware,
            "capabilities": self.capabilities
        }


class LLMRouter:
    """
    Router for LLM provider selection and request handling.
    
    This class manages the routing of requests to different LLM providers
    based on configuration settings, availability, and optimization criteria.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the LLM router.
        
        Args:
            config: Configuration dictionary for the router
        """
        self.config = config or {}
        self._init_providers()
    
    def _init_providers(self) -> None:
        """Initialize LLM providers based on configuration."""
        self.providers = []
        
        # Read from environment or config
        provider_list = os.environ.get(
            "LLM_PROVIDERS", 
            self.config.get("llm_providers", "openai,local")
        )
        
        for provider in provider_list.split(","):
            provider = provider.strip().lower()
            if provider == LLMProvider.OPENAI:
                if self._check_openai_available():
                    self.providers.append(LLMProvider.OPENAI)
            elif provider == LLMProvider.ANTHROPIC:
                if self._check_anthropic_available():
                    self.providers.append(LLMProvider.ANTHROPIC)
            elif provider == LLMProvider.LOCAL:
                if self._check_local_available():
                    self.providers.append(LLMProvider.LOCAL)
        
        if not self.providers:
            logger.warning("No LLM providers are available. Some functionality may be limited.")
    
    def _check_openai_available(self) -> bool:
        """Check if OpenAI API is available."""
        api_key = os.environ.get("OPENAI_API_KEY", self.config.get("openai_api_key"))
        if not api_key:
            logger.warning("OpenAI API key not found. OpenAI provider will be disabled.")
            return False
        
        try:
            import openai
            return True
        except ImportError:
            logger.warning("OpenAI Python package not installed. OpenAI provider will be disabled.")
            return False
    
    def _check_anthropic_available(self) -> bool:
        """Check if Anthropic API is available."""
        api_key = os.environ.get("ANTHROPIC_API_KEY", self.config.get("anthropic_api_key"))
        if not api_key:
            logger.warning("Anthropic API key not found. Anthropic provider will be disabled.")
            return False
        
        try:
            import anthropic
            return True
        except ImportError:
            logger.warning("Anthropic Python package not installed. Anthropic provider will be disabled.")
            return False
    
    def _check_local_available(self) -> bool:
        """Check if local LLM models are available."""
        model_path = os.environ.get("LLM_LOCAL_MODEL_PATH", self.config.get("llm_local_model_path"))
        
        if not model_path:
            logger.warning("Local model path not configured. Local provider will be disabled.")
            return False
        
        try:
            import mlx  # Try to import MLX for local models
            return os.path.exists(model_path)
        except ImportError:
            try:
                # Try llama.cpp as fallback
                import llama_cpp
                return os.path.exists(model_path)
            except ImportError:
                logger.warning("Neither MLX nor llama.cpp package installed. Local provider will be disabled.")
                return False
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of available LLM models across all providers.
        
        Returns:
            List of dictionaries containing model information
        """
        models = []
        
        # OpenAI models
        if LLMProvider.OPENAI in self.providers:
            models.extend([
                LLMModel(
                    name="gpt-4o",
                    provider=LLMProvider.OPENAI,
                    context_size=128000,
                    hardware="OpenAI API",
                    input_cost_per_1k_tokens=0.01,
                    output_cost_per_1k_tokens=0.03,
                    capabilities=["text", "vision", "function_calling"],
                ).to_dict(),
                LLMModel(
                    name="gpt-4-turbo",
                    provider=LLMProvider.OPENAI,
                    context_size=128000,
                    hardware="OpenAI API",
                    input_cost_per_1k_tokens=0.01,
                    output_cost_per_1k_tokens=0.03,
                    capabilities=["text", "vision", "function_calling"],
                ).to_dict(),
                LLMModel(
                    name="gpt-3.5-turbo",
                    provider=LLMProvider.OPENAI,
                    context_size=16385,
                    hardware="OpenAI API",
                    input_cost_per_1k_tokens=0.0005,
                    output_cost_per_1k_tokens=0.0015,
                    capabilities=["text", "function_calling"],
                ).to_dict(),
            ])
        
        # Anthropic models
        if LLMProvider.ANTHROPIC in self.providers:
            models.extend([
                LLMModel(
                    name="claude-3-opus",
                    provider=LLMProvider.ANTHROPIC,
                    context_size=200000,
                    hardware="Anthropic API",
                    input_cost_per_1k_tokens=0.015,
                    output_cost_per_1k_tokens=0.075,
                    capabilities=["text", "vision"],
                ).to_dict(),
                LLMModel(
                    name="claude-3-sonnet",
                    provider=LLMProvider.ANTHROPIC,
                    context_size=200000,
                    hardware="Anthropic API",
                    input_cost_per_1k_tokens=0.003,
                    output_cost_per_1k_tokens=0.015,
                    capabilities=["text", "vision"],
                ).to_dict(),
                LLMModel(
                    name="claude-3-haiku",
                    provider=LLMProvider.ANTHROPIC,
                    context_size=200000,
                    hardware="Anthropic API",
                    input_cost_per_1k_tokens=0.00025,
                    output_cost_per_1k_tokens=0.00125,
                    capabilities=["text", "vision"],
                ).to_dict(),
            ])
        
        # Local models - dynamically discovered
        if LLMProvider.LOCAL in self.providers:
            local_models = self._discover_local_models()
            models.extend(local_models)
        
        return models
    
    def _discover_local_models(self) -> List[Dict[str, Any]]:
        """
        Discover local LLM models.
        
        Returns:
            List of dictionaries containing model information
        """
        models = []
        model_path = os.environ.get("LLM_LOCAL_MODEL_PATH", self.config.get("llm_local_model_path", ""))
        
        if os.path.exists(model_path):
            # Check for .gguf files for llama.cpp compatibility
            gguf_files = [f for f in os.listdir(model_path) if f.endswith(".gguf")]
            for model_file in gguf_files:
                model_name = os.path.splitext(model_file)[0]
                models.append(
                    LLMModel(
                        name=model_name,
                        provider=LLMProvider.LOCAL,
                        context_size=4096,  # Default, may vary by model
                        hardware="CPU/GPU (llama.cpp)",
                        capabilities=["text"],
                        cost_per_1k_tokens=0.0,  # Local models are free to run
                    ).to_dict()
                )
            
            # Check for MLX model directories
            subdirs = [f for f in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, f))]
            for subdir in subdirs:
                if os.path.exists(os.path.join(model_path, subdir, "config.json")):
                    models.append(
                        LLMModel(
                            name=subdir,
                            provider=LLMProvider.LOCAL,
                            context_size=4096,  # Default, may vary by model
                            hardware="Apple Silicon (MLX)",
                            capabilities=["text"],
                            cost_per_1k_tokens=0.0,  # Local models are free to run
                        ).to_dict()
                    )
        
        return models
    
    def select_model(self, 
                    task: str, 
                    preferred_provider: Optional[LLMProvider] = None, 
                    required_capabilities: List[str] = None) -> Optional[Dict[str, Any]]:
        """
        Select the most appropriate model for a given task.
        
        Args:
            task: Description of the task to be performed
            preferred_provider: Preferred LLM provider if available
            required_capabilities: List of required capabilities (e.g., ["text", "vision"])
            
        Returns:
            Dictionary with model information or None if no suitable model found
        """
        required_capabilities = required_capabilities or ["text"]
        available_models = self.get_available_models()
        
        # Filter by capabilities
        capable_models = []
        for model in available_models:
            has_capabilities = all(cap in model.get("capabilities", []) for cap in required_capabilities)
            if has_capabilities:
                capable_models.append(model)
        
        if not capable_models:
            logger.warning(f"No models found with required capabilities: {required_capabilities}")
            return None
        
        # Filter by preferred provider if specified
        if preferred_provider:
            provider_models = [m for m in capable_models if m["provider"] == preferred_provider]
            if provider_models:
                capable_models = provider_models
        
        # Simple cost-based selection - choose cheapest model with required capabilities
        # In a more sophisticated implementation, this could consider:
        # - Task complexity vs. model capabilities
        # - Response time requirements
        # - Cost constraints
        if capable_models:
            # For simplicity, this selects the first model, but could be enhanced with
            # more sophisticated selection logic
            return capable_models[0]
        
        return None


def get_available_models() -> List[Dict[str, Any]]:
    """
    Get list of available LLM models across all providers.
    
    This is a convenience function that creates a router and returns the list
    of available models.
    
    Returns:
        List of dictionaries containing model information
    """
    router = LLMRouter()
    return router.get_available_models()


def get_model_for_task(task: str, 
                       preferred_provider: Optional[str] = None,
                       required_capabilities: List[str] = None) -> Optional[Dict[str, Any]]:
    """
    Select the most appropriate model for a given task.
    
    Args:
        task: Description of the task to be performed
        preferred_provider: Preferred LLM provider if available (openai, anthropic, local)
        required_capabilities: List of required capabilities (e.g., ["text", "vision"])
        
    Returns:
        Dictionary with model information or None if no suitable model found
    """
    router = LLMRouter()
    provider = LLMProvider(preferred_provider) if preferred_provider else None
    return router.select_model(task, provider, required_capabilities) 