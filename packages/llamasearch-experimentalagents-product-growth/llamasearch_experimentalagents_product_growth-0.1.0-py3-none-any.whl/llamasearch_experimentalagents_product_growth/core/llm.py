"""
LLM convenience module for LlamaSearch ExperimentalAgents: Product Growth.

This module provides high-level functions for working with LLMs through
the router and client implementations.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union

from .llm_router import (
    LLMRouter, 
    LLMProvider, 
    get_available_models, 
    get_model_for_task
)
from .llm_client import (
    LLMClient,
    LLMMessage,
    LLMFunction,
    LLMResponse,
    create_client
)

logger = logging.getLogger(__name__)


def complete_prompt(prompt: str, 
                   system_prompt: Optional[str] = None,
                   model: Optional[str] = None,
                   provider: Optional[str] = None,
                   temperature: float = 0.7,
                   max_tokens: Optional[int] = None) -> str:
    """
    Simple function to complete a prompt with an LLM.
    
    Args:
        prompt: User prompt to complete
        system_prompt: Optional system prompt to prepend
        model: Specific model to use (if None, will be auto-selected)
        provider: Specific provider to use (if None, will be auto-selected)
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated text
    """
    messages = []
    
    if system_prompt:
        messages.append(LLMMessage.system(system_prompt))
    
    messages.append(LLMMessage.user(prompt))
    
    # Auto-select model if not specified
    if not model or not provider:
        selected_model = get_model_for_task(
            task="Text completion",
            preferred_provider=provider
        )
        
        if not selected_model:
            raise ValueError("No suitable LLM model found")
        
        provider = selected_model["provider"]
        model = model or selected_model["name"]
    
    # Create client and get completion
    client = create_client(provider=provider, model=model)
    response = client.complete(
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response.content


def chat_completion(messages: List[Union[Dict[str, Any], LLMMessage]], 
                  functions: Optional[List[Union[Dict[str, Any], LLMFunction]]] = None,
                  model: Optional[str] = None,
                  provider: Optional[str] = None,
                  temperature: float = 0.7,
                  max_tokens: Optional[int] = None) -> LLMResponse:
    """
    Generate a chat completion with an LLM.
    
    Args:
        messages: List of messages for the conversation
        functions: Optional list of functions/tools to make available to the LLM
        model: Specific model to use (if None, will be auto-selected)
        provider: Specific provider to use (if None, will be auto-selected)
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate
        
    Returns:
        LLMResponse object with the completion
    """
    # Auto-select model if not specified
    required_capabilities = ["text"]
    if functions:
        required_capabilities.append("function_calling")
    
    if not model or not provider:
        selected_model = get_model_for_task(
            task="Chat completion", 
            preferred_provider=provider,
            required_capabilities=required_capabilities
        )
        
        if not selected_model:
            # If function calling is requested but not available, try without it
            if "function_calling" in required_capabilities:
                required_capabilities.remove("function_calling")
                selected_model = get_model_for_task(
                    task="Chat completion",
                    preferred_provider=provider,
                    required_capabilities=required_capabilities
                )
                
                if selected_model:
                    logger.warning("Function calling capability not available with selected model")
                    functions = None
        
        if not selected_model:
            raise ValueError("No suitable LLM model found")
        
        provider = selected_model["provider"]
        model = model or selected_model["name"]
    
    # Create client and get completion
    client = create_client(provider=provider, model=model)
    return client.complete(
        messages=messages,
        functions=functions,
        temperature=temperature,
        max_tokens=max_tokens
    )


def analyze_text(text: str, 
               analysis_type: str = "sentiment", 
               model: Optional[str] = None,
               provider: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze text using an LLM.
    
    Args:
        text: Text to analyze
        analysis_type: Type of analysis to perform (sentiment, themes, etc.)
        model: Specific model to use (if None, will be auto-selected)
        provider: Specific provider to use (if None, will be auto-selected)
        
    Returns:
        Dictionary with analysis results
    """
    prompt_templates = {
        "sentiment": (
            "Analyze the sentiment of the following text. "
            "Return a JSON object with 'score' (float between -1 and 1), "
            "'label' (positive, negative, or neutral), and 'explanation' keys.\n\n"
            "Text to analyze:\n{text}"
        ),
        "themes": (
            "Identify the main themes in the following text. "
            "Return a JSON array of theme objects, each with 'name' and 'relevance' (0-1) keys.\n\n"
            "Text to analyze:\n{text}"
        ),
        "entities": (
            "Extract named entities from the following text. "
            "Return a JSON array of entity objects, each with 'text', 'type', and 'relevance' (0-1) keys.\n\n"
            "Text to analyze:\n{text}"
        ),
        "summary": (
            "Summarize the following text in a concise manner. "
            "Return a JSON object with 'summary' and 'key_points' (array) keys.\n\n"
            "Text to summarize:\n{text}"
        )
    }
    
    if analysis_type not in prompt_templates:
        raise ValueError(f"Unsupported analysis type: {analysis_type}")
    
    prompt = prompt_templates[analysis_type].format(text=text)
    system_prompt = (
        "You are an expert text analyst. Your task is to analyze the provided text "
        "and return a JSON object with the analysis results. Do not include any explanations "
        "or markdown formatting, just return the JSON object."
    )
    
    response = complete_prompt(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        provider=provider,
        temperature=0.1  # Low temperature for more deterministic analysis
    )
    
    try:
        import json
        # Try to parse the response as JSON
        result = json.loads(response)
        return result
    except json.JSONDecodeError:
        # Fallback: return the text response
        logger.warning("Could not parse LLM response as JSON")
        return {"raw_response": response}


def generate_strategies(feedback_analysis: Dict[str, Any], 
                      max_strategies: int = 5,
                      model: Optional[str] = None,
                      provider: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Generate growth strategies based on feedback analysis.
    
    Args:
        feedback_analysis: Analysis of customer feedback
        max_strategies: Maximum number of strategies to generate
        model: Specific model to use (if None, will be auto-selected)
        provider: Specific provider to use (if None, will be auto-selected)
        
    Returns:
        List of strategy dictionaries
    """
    prompt = (
        "Based on the provided customer feedback analysis, generate up to "
        f"{max_strategies} product growth strategies. Each strategy should include "
        "a feature or improvement name, priority level (high, medium, low), "
        "expected impact (0-1), and applicable go-to-market approaches.\n\n"
        "Return a JSON array of strategy objects.\n\n"
        f"Feedback Analysis:\n{feedback_analysis}"
    )
    
    system_prompt = (
        "You are a product growth strategist specializing in turning customer feedback "
        "into actionable growth strategies. Your task is to analyze the feedback clusters "
        "and sentiment data, then recommend specific features or improvements that would "
        "drive product growth. Focus on strategies that address negative sentiment areas "
        "or enhance already positive aspects of the product."
    )
    
    # Use a higher temperature for more creative strategies
    response = complete_prompt(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        provider=provider,
        temperature=0.8,
        max_tokens=2000
    )
    
    try:
        import json
        # Try to parse the response as JSON
        result = json.loads(response)
        
        # Ensure we don't exceed max_strategies
        return result[:max_strategies]
    except json.JSONDecodeError:
        # Fallback: return an error message
        logger.error("Could not parse strategies from LLM response")
        return [{"error": "Failed to generate strategies", "raw_response": response}] 