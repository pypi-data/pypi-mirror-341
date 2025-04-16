# LLM Router

The LLM Router is a key component of the LlamaSearch ExperimentalAgents Product Growth system, providing seamless integration with multiple LLM providers and handling fallback mechanisms when preferred providers are unavailable.

## Overview

The LLM Router allows your application to:

1. Work with multiple LLM providers (OpenAI, Anthropic, local models)
2. Automatically select the most appropriate model based on the task requirements
3. Fall back to alternative providers when the preferred one is unavailable
4. Discover and use local models when available

## Architecture

The LLM Router consists of three main components:

1. **LLM Router**: Core routing logic that selects appropriate models based on availability and capabilities
2. **LLM Client**: Provider-specific client implementations that handle the actual API calls
3. **High-level Utilities**: Convenience functions for common tasks like completions and analysis

### Class Diagram

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│ LLMProvider │     │   LLMRouter   │     │   LLMModel   │
└─────────────┘     └───────────────┘     └──────────────┘
       ▲                    │                    
       │                    │                    
       │                    ▼                    
┌─────────────┐     ┌───────────────┐           
│  LLMClient  │◄────│ create_client │           
└─────────────┘     └───────────────┘           
       ▲                                        
       │                                        
┌──────┴──────┬────────────────┬───────────────┐
│             │                │               │
│ OpenAIClient│AnthropicClient │LocalModelClient│
└─────────────┴────────────────┴───────────────┘
```

## Configuration

The LLM Router can be configured through environment variables or directly via the API:

```bash
# Set in .env file or environment
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Provider selection and fallback order
LLM_PROVIDERS=openai,anthropic,local
LLM_LOCAL_MODEL_PATH=/path/to/local/models
```

## Basic Usage

```python
from llamasearch_experimentalagents_product_growth.core import (
    complete_prompt, chat_completion, analyze_text
)

# Auto-select the best available model
response = complete_prompt(
    prompt="Summarize this product feedback",
    system_prompt="You are a product analyst."
)

# Specify a provider preference
response = complete_prompt(
    prompt="What are the main themes in this feedback?",
    provider="anthropic",
    model="claude-3-haiku"
)
```

## Provider Selection Process

When selecting a provider, the LLM Router follows this process:

1. Check which providers are available based on API keys and dependencies
2. Filter providers based on the required capabilities (e.g., function calling)
3. Use the preferred provider if specified and available
4. Fall back to other available providers in the order specified in `LLM_PROVIDERS`

## Provider-Specific Features

### OpenAI

```python
# Function calling with OpenAI models
from llamasearch_experimentalagents_product_growth.core import chat_completion
from llamasearch_experimentalagents_product_growth.core import LLMMessage, LLMFunction

messages = [
    LLMMessage.user("What's the weather in New York?")
]

functions = [
    LLMFunction(
        name="get_weather", 
        description="Get the weather in a location",
        parameters={"location": {"type": "string"}}
    )
]

response = chat_completion(
    messages=messages,
    functions=functions,
    provider="openai"
)

if response.function_call:
    print(f"Function: {response.function_call['name']}")
    print(f"Arguments: {response.function_call['arguments']}")
```

### Anthropic

```python
# Vision capabilities with Anthropic models
from llamasearch_experimentalagents_product_growth.core import chat_completion
from llamasearch_experimentalagents_product_growth.core import LLMMessage

messages = [
    LLMMessage.system("You are a helpful assistant."),
    LLMMessage.user("What's in this image? [image-url]")
]

response = chat_completion(
    messages=messages,
    provider="anthropic",
    model="claude-3-opus"
)
```

### Local Models

```python
# Use local models for cost-free inference
from llamasearch_experimentalagents_product_growth.core import complete_prompt

# Will use local model if available and specified in LLM_PROVIDERS
response = complete_prompt(
    prompt="Summarize this text",
    provider="local"
)
```

## Advanced Usage: Custom Router Configuration

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMRouter

# Create a router with custom configuration
router = LLMRouter(config={
    "llm_providers": "openai,local",
    "openai_api_key": "your-key-here",
    "llm_local_model_path": "/custom/path/to/models"
})

# Get available models
models = router.get_available_models()

# Select a model for a specific task
model = router.select_model(
    task="Sensitive data analysis",
    preferred_provider="local",  # Prefer local models for sensitive data
    required_capabilities=["text"]
)
```

## Performance Considerations

- The router caches provider availability to avoid repeated checks
- Local models are used when API latency is a concern
- For batch processing, reuse the same client instance rather than creating new ones

## Error Handling

The LLM Router provides robust error handling:

```python
try:
    response = complete_prompt(
        prompt="Complex analysis task",
        provider="openai"
    )
except ValueError as e:
    # Handle configuration errors
    print(f"Configuration error: {e}")
    # Fall back to a different provider
    response = complete_prompt(
        prompt="Complex analysis task",
        provider="anthropic"
    )
except Exception as e:
    # Handle API errors
    print(f"API error: {e}")
    # Fall back to rule-based approach
    response = "Unable to process with LLM"
```

## Extending with New Providers

The LLM Router is designed for extensibility. To add a new provider:

1. Add a new value to the `LLMProvider` enum
2. Create a new client class extending `LLMClient`
3. Update the `create_client` factory function
4. Add provider detection in the `_init_providers` method

## Best Practices

1. **Configuration**: Store API keys in environment variables, not in code
2. **Fallbacks**: Always provide fallback mechanisms when using LLMs
3. **Model Selection**: Let the router select the appropriate model when possible
4. **Error Handling**: Handle API errors gracefully with fallbacks
5. **Local Models**: Use local models for sensitive data or offline operation 