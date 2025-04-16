"""
LLM Client for LlamaSearch ExperimentalAgents: Product Growth.

This module provides client implementations for interacting with various
LLM providers including OpenAI, Anthropic, and local models.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union, Callable
from enum import Enum

from .llm_router import LLMProvider

logger = logging.getLogger(__name__)

class LLMMessage:
    """Message format for LLM interactions."""
    
    ROLE_SYSTEM = "system"
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_FUNCTION = "function"
    
    def __init__(self, 
                 role: str, 
                 content: str, 
                 name: Optional[str] = None, 
                 function_call: Optional[Dict[str, Any]] = None):
        """
        Initialize a message.
        
        Args:
            role: Role of the message (system, user, assistant, function)
            content: Content of the message
            name: Name of the function (for function messages)
            function_call: Function call information (for assistant messages)
        """
        self.role = role
        self.content = content
        self.name = name
        self.function_call = function_call
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to provider-agnostic dictionary format."""
        result = {
            "role": self.role,
            "content": self.content
        }
        
        if self.name:
            result["name"] = self.name
            
        if self.function_call:
            result["function_call"] = self.function_call
            
        return result
    
    @classmethod
    def system(cls, content: str) -> 'LLMMessage':
        """Create a system message."""
        return cls(role=cls.ROLE_SYSTEM, content=content)
    
    @classmethod
    def user(cls, content: str) -> 'LLMMessage':
        """Create a user message."""
        return cls(role=cls.ROLE_USER, content=content)
    
    @classmethod
    def assistant(cls, content: str, function_call: Optional[Dict[str, Any]] = None) -> 'LLMMessage':
        """Create an assistant message."""
        return cls(role=cls.ROLE_ASSISTANT, content=content, function_call=function_call)
    
    @classmethod
    def function(cls, name: str, content: str) -> 'LLMMessage':
        """Create a function message with function output."""
        return cls(role=cls.ROLE_FUNCTION, content=content, name=name)


class LLMFunction:
    """Function definition for LLM function calling."""
    
    def __init__(self, 
                 name: str, 
                 description: str, 
                 parameters: Dict[str, Any],
                 required: Optional[List[str]] = None):
        """
        Initialize a function definition.
        
        Args:
            name: Name of the function
            description: Description of what the function does
            parameters: JSON Schema for the function parameters
            required: List of required parameter names
        """
        self.name = name
        self.description = description
        self.parameters = parameters
        self.required = required or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to provider-agnostic dictionary format."""
        params_dict = {
            "type": "object",
            "properties": self.parameters
        }
        
        if self.required:
            params_dict["required"] = self.required
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": params_dict
        }


class LLMResponse:
    """Response from an LLM completion."""
    
    def __init__(self, 
                 content: str, 
                 function_call: Optional[Dict[str, Any]] = None,
                 message_id: Optional[str] = None,
                 usage: Optional[Dict[str, int]] = None,
                 model: Optional[str] = None):
        """
        Initialize a response.
        
        Args:
            content: Text content of the response
            function_call: Function call information if any
            message_id: ID of the message
            usage: Token usage statistics
            model: Model used for the response
        """
        self.content = content
        self.function_call = function_call
        self.message_id = message_id
        self.usage = usage or {}
        self.model = model
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result = {
            "content": self.content,
            "model": self.model,
            "usage": self.usage
        }
        
        if self.function_call:
            result["function_call"] = self.function_call
            
        if self.message_id:
            result["message_id"] = self.message_id
            
        return result


class LLMClient:
    """Base class for LLM clients."""
    
    def __init__(self, model: str, api_key: Optional[str] = None):
        """
        Initialize the client.
        
        Args:
            model: Name of the model to use
            api_key: API key for authentication (if required)
        """
        self.model = model
        self.api_key = api_key
    
    def complete(self, 
                messages: List[Union[LLMMessage, Dict[str, Any]]], 
                functions: Optional[List[Union[LLMFunction, Dict[str, Any]]]] = None,
                temperature: float = 0.7,
                max_tokens: Optional[int] = None) -> LLMResponse:
        """
        Generate a completion based on the provided messages.
        
        Args:
            messages: List of messages for context
            functions: List of functions available to the model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Response from the model
        """
        raise NotImplementedError("Subclasses must implement this method")


class OpenAIClient(LLMClient):
    """Client for OpenAI API."""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        """
        Initialize the OpenAI client.
        
        Args:
            model: OpenAI model name
            api_key: OpenAI API key
        """
        super().__init__(model, api_key)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    def complete(self, 
                messages: List[Union[LLMMessage, Dict[str, Any]]], 
                functions: Optional[List[Union[LLMFunction, Dict[str, Any]]]] = None,
                temperature: float = 0.7,
                max_tokens: Optional[int] = None) -> LLMResponse:
        """
        Generate a completion using OpenAI API.
        
        Args:
            messages: List of messages for context
            functions: List of functions available to the model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Response from the model
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Convert messages to OpenAI format
            openai_messages = []
            for msg in messages:
                if isinstance(msg, LLMMessage):
                    openai_messages.append(msg.to_dict())
                else:
                    openai_messages.append(msg)
            
            # Prepare the request parameters
            params = {
                "model": self.model,
                "messages": openai_messages,
                "temperature": temperature,
            }
            
            if max_tokens:
                params["max_tokens"] = max_tokens
            
            # Add functions if provided
            if functions:
                openai_functions = []
                for func in functions:
                    if isinstance(func, LLMFunction):
                        openai_functions.append(func.to_dict())
                    else:
                        openai_functions.append(func)
                
                params["functions"] = openai_functions
            
            # Make the API call
            response = client.chat.completions.create(**params)
            
            # Extract the response content and function call if any
            choice = response.choices[0]
            content = choice.message.content or ""
            
            function_call = None
            if hasattr(choice.message, "function_call") and choice.message.function_call:
                function_call = {
                    "name": choice.message.function_call.name,
                    "arguments": choice.message.function_call.arguments
                }
            
            # Create response object
            return LLMResponse(
                content=content,
                function_call=function_call,
                message_id=response.id,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                model=self.model
            )
            
        except ImportError:
            raise ImportError("OpenAI package is not installed. Install with `pip install openai`")
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            raise


class AnthropicClient(LLMClient):
    """Client for Anthropic API."""
    
    def __init__(self, model: str = "claude-3-sonnet-20240229", api_key: Optional[str] = None):
        """
        Initialize the Anthropic client.
        
        Args:
            model: Anthropic model name
            api_key: Anthropic API key
        """
        super().__init__(model, api_key)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
    
    def complete(self, 
                messages: List[Union[LLMMessage, Dict[str, Any]]], 
                functions: Optional[List[Union[LLMFunction, Dict[str, Any]]]] = None,
                temperature: float = 0.7,
                max_tokens: Optional[int] = None) -> LLMResponse:
        """
        Generate a completion using Anthropic API.
        
        Args:
            messages: List of messages for context
            functions: List of functions available to the model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Response from the model
        """
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Convert messages to Anthropic format
            anthropic_messages = []
            for msg in messages:
                if isinstance(msg, LLMMessage):
                    msg_dict = msg.to_dict()
                    # Anthropic uses "assistant" role instead of "function"
                    if msg_dict["role"] == "function":
                        msg_dict["role"] = "assistant"
                    anthropic_messages.append(msg_dict)
                else:
                    anthropic_messages.append(msg)
            
            # Prepare the request parameters
            params = {
                "model": self.model,
                "messages": anthropic_messages,
                "temperature": temperature,
            }
            
            # Convert max_tokens to max_tokens_to_sample for Anthropic
            if max_tokens:
                params["max_tokens"] = max_tokens
            
            # Note: Anthropic has a different approach to tool/function calling
            # This implementation may need to be updated as their API evolves
            if functions:
                tools = []
                for func in functions:
                    if isinstance(func, LLMFunction):
                        func_dict = func.to_dict()
                    else:
                        func_dict = func
                    
                    tools.append({
                        "name": func_dict["name"],
                        "description": func_dict["description"],
                        "input_schema": func_dict["parameters"]
                    })
                
                params["tools"] = tools
            
            # Make the API call
            response = client.messages.create(**params)
            
            # Extract the response content and tool calls if any
            content = response.content[0].text
            
            function_call = None
            if hasattr(response, "tool_calls") and response.tool_calls:
                # Take the first tool call for simplicity
                tool_call = response.tool_calls[0]
                function_call = {
                    "name": tool_call.name,
                    "arguments": tool_call.input
                }
            
            # Create response object
            return LLMResponse(
                content=content,
                function_call=function_call,
                message_id=response.id,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                model=self.model
            )
            
        except ImportError:
            raise ImportError("Anthropic package is not installed. Install with `pip install anthropic`")
        except Exception as e:
            logger.error(f"Error in Anthropic API call: {str(e)}")
            raise


class LocalModelClient(LLMClient):
    """Client for local LLM models."""
    
    def __init__(self, model: str, model_path: Optional[str] = None):
        """
        Initialize the local model client.
        
        Args:
            model: Name of the model file or directory
            model_path: Path to the model directory (optional)
        """
        super().__init__(model, None)
        self.model_path = model_path or os.environ.get("LLM_LOCAL_MODEL_PATH", "")
        
        if not self.model_path:
            raise ValueError("Local model path is required")
        
        self._init_model()
    
    def _init_model(self):
        """Initialize the local model based on available libraries."""
        model_file = os.path.join(self.model_path, self.model)
        
        # Try to use MLX first
        try:
            import mlx
            # MLX-based model initialization would go here
            # This is a simplified placeholder
            self._model_type = "mlx"
            return
        except ImportError:
            pass
        
        # Try to use llama.cpp
        try:
            from llama_cpp import Llama
            
            # Check if it's a GGUF file
            if self.model.endswith(".gguf") or os.path.exists(f"{model_file}.gguf"):
                model_path = self.model if self.model.endswith(".gguf") else f"{model_file}.gguf"
                self._model = Llama(model_path=model_path)
                self._model_type = "llama_cpp"
                return
        except ImportError:
            pass
        
        raise ValueError(f"Could not initialize local model: {self.model}. No supported framework found.")
    
    def complete(self, 
                messages: List[Union[LLMMessage, Dict[str, Any]]], 
                functions: Optional[List[Union[LLMFunction, Dict[str, Any]]]] = None,
                temperature: float = 0.7,
                max_tokens: Optional[int] = None) -> LLMResponse:
        """
        Generate a completion using a local model.
        
        Args:
            messages: List of messages for context
            functions: List of functions available to the model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Response from the model
        """
        # Convert messages to a simple prompt for local models
        # This is a simplified approach and could be enhanced
        prompt = ""
        for msg in messages:
            if isinstance(msg, LLMMessage):
                msg_dict = msg.to_dict()
            else:
                msg_dict = msg
            
            if msg_dict["role"] == "system":
                prompt += f"SYSTEM: {msg_dict['content']}\n\n"
            elif msg_dict["role"] == "user":
                prompt += f"USER: {msg_dict['content']}\n\n"
            elif msg_dict["role"] == "assistant":
                prompt += f"ASSISTANT: {msg_dict['content']}\n\n"
        
        prompt += "ASSISTANT: "
        
        # Generate completion based on model type
        if self._model_type == "llama_cpp":
            max_tokens = max_tokens or 512
            result = self._model.create_completion(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return LLMResponse(
                content=result["choices"][0]["text"],
                model=self.model
            )
        
        elif self._model_type == "mlx":
            # Placeholder for MLX model generation
            # This would be implemented based on MLX's API
            return LLMResponse(
                content="[MLX model output would appear here]",
                model=self.model
            )
        
        else:
            raise ValueError(f"Unsupported model type: {self._model_type}")


def create_client(provider: str, model: str, api_key: Optional[str] = None) -> LLMClient:
    """
    Create an LLM client based on the provider.
    
    Args:
        provider: LLM provider name (openai, anthropic, local)
        model: Model name to use
        api_key: API key for the provider (if required)
        
    Returns:
        LLM client instance
    """
    if provider == LLMProvider.OPENAI:
        return OpenAIClient(model=model, api_key=api_key)
    elif provider == LLMProvider.ANTHROPIC:
        return AnthropicClient(model=model, api_key=api_key)
    elif provider == LLMProvider.LOCAL:
        return LocalModelClient(model=model)
    else:
        raise ValueError(f"Unsupported provider: {provider}") 