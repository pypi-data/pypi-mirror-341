# Using the LLM Router

The LLM Router is a powerful component that provides seamless access to multiple LLM providers. This guide explains how to use it effectively in your applications.

## Basic Usage

The simplest way to use the LLM router is through the high-level utility functions:

```python
from llamasearch_experimentalagents_product_growth.core import complete_prompt

# Simple completion (auto-selects best available model)
response = complete_prompt(
    prompt="Summarize the benefits of AI in product growth",
    system_prompt="You are a product strategy expert."
)

print(response)
```

## Specifying Providers

You can specify which provider to use:

```python
from llamasearch_experimentalagents_product_growth.core import complete_prompt

# Use OpenAI
openai_response = complete_prompt(
    prompt="Generate three product improvement ideas",
    provider="openai",
    model="gpt-4o"  # Optional: specify model
)

# Use Anthropic
anthropic_response = complete_prompt(
    prompt="Generate three product improvement ideas",
    provider="anthropic",
    model="claude-3-sonnet"  # Optional: specify model
)

# Use local model (if available)
local_response = complete_prompt(
    prompt="Generate three product improvement ideas",
    provider="local"
)
```

## Chat Completions

For more complex interactions, use the chat completion function:

```python
from llamasearch_experimentalagents_product_growth.core import chat_completion
from llamasearch_experimentalagents_product_growth.core import LLMMessage

messages = [
    LLMMessage.system("You are a product growth expert."),
    LLMMessage.user("What are the best strategies for increasing user engagement?"),
    LLMMessage.assistant("There are several effective strategies. Which industry are you in?"),
    LLMMessage.user("SaaS productivity tools")
]

response = chat_completion(
    messages=messages,
    temperature=0.7  # Control creativity/randomness
)

print(response.content)
```

## Function Calling

You can use function calling capabilities with supported models:

```python
from llamasearch_experimentalagents_product_growth.core import chat_completion
from llamasearch_experimentalagents_product_growth.core import LLMMessage, LLMFunction

# Define functions
get_metrics = LLMFunction(
    name="get_metrics",
    description="Get performance metrics for a product feature",
    parameters={
        "feature_name": {
            "type": "string",
            "description": "Name of the feature to get metrics for"
        },
        "time_period": {
            "type": "string",
            "enum": ["day", "week", "month", "quarter", "year"],
            "description": "Time period for the metrics"
        }
    },
    required=["feature_name"]
)

# Create conversation
messages = [
    LLMMessage.system("You are a product analytics assistant."),
    LLMMessage.user("What are the performance metrics for our search feature?")
]

# Get response with function calling
response = chat_completion(
    messages=messages,
    functions=[get_metrics],
    provider="openai"  # Function calling works best with OpenAI
)

# Check if the model wants to call a function
if response.function_call:
    function_name = response.function_call["name"]
    arguments = response.function_call["arguments"]
    print(f"Function call: {function_name}")
    print(f"Arguments: {arguments}")
    
    # In a real application, you would execute the function here
    # and then send the result back to the model
    
    # Example of sending function result back:
    result = '{"daily_active_users": 1250, "retention": 0.82, "engagement_score": 8.5}'
    messages.append(LLMMessage.assistant(
        content="",
        function_call=response.function_call
    ))
    messages.append(LLMMessage.function(
        name=function_name,
        content=result
    ))
    
    # Get final response with function result
    final_response = chat_completion(
        messages=messages,
        functions=[get_metrics],
        provider="openai"
    )
    
    print(f"Final response: {final_response.content}")
```

## Text Analysis

Use the analyze_text utility for common analysis tasks:

```python
from llamasearch_experimentalagents_product_growth.core import analyze_text

# Analyze sentiment
sentiment_result = analyze_text(
    text="I absolutely love this feature! It saves me so much time.",
    analysis_type="sentiment"
)
print(f"Sentiment score: {sentiment_result['score']}")
print(f"Label: {sentiment_result['label']}")

# Extract themes
themes_result = analyze_text(
    text="The UI is intuitive but performance is slow when loading large datasets.",
    analysis_type="themes"
)
for theme in themes_result:
    print(f"Theme: {theme['name']} (relevance: {theme['relevance']})")

# Summarize text
summary_result = analyze_text(
    text="Long customer feedback...",
    analysis_type="summary"
)
print(f"Summary: {summary_result['summary']}")
```

## Generating Growth Strategies

The generate_strategies function uses LLMs to create product growth recommendations:

```python
from llamasearch_experimentalagents_product_growth.core import generate_strategies

# Feedback analysis data
analysis_results = {
    "num_clusters": 3,
    "cluster_sentiments": {"0": 0.8, "1": -0.3, "2": -0.7},
    "cluster_themes": {
        "0": ["pricing", "value"],
        "1": ["user interface", "design"],
        "2": ["performance", "speed"]
    }
}

# Generate strategies
strategies = generate_strategies(
    feedback_analysis=analysis_results,
    max_strategies=5,
    provider="openai",
    model="gpt-4o"  # For best results
)

# Display strategies
for strategy in strategies:
    print(f"\nStrategy: {strategy['feature']}")
    print(f"Priority: {strategy['priority']}")
    print(f"Impact: {strategy['expected_impact']}")
    print(f"GTM Approaches: {', '.join(strategy['gtm_strategies'])}")
```

## Configuration

Configure the LLM router through environment variables:

```bash
# .env file
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
LLM_PROVIDERS=openai,anthropic,local
LLM_LOCAL_MODEL_PATH=/path/to/local/models
```

Or directly via code:

```python
import os
from llamasearch_experimentalagents_product_growth.core import complete_prompt

# Set environment variables programmatically
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["LLM_PROVIDERS"] = "openai,local"

response = complete_prompt("Your prompt here")
```

## Advanced: Direct Router Access

For more control, you can use the router directly:

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import (
    LLMRouter,
    LLMProvider,
    get_available_models
)
from llamasearch_experimentalagents_product_growth.core.llm_client import create_client

# Initialize router with custom configuration
router = LLMRouter(config={
    "llm_providers": "openai,anthropic,local",
    "openai_api_key": "your-openai-key",
    "anthropic_api_key": "your-anthropic-key"
})

# Get available models
available_models = router.get_available_models()
for model in available_models:
    print(f"{model['name']} ({model['provider']})")

# Select model for specific task
selected_model = router.select_model(
    task="Generate creative content",
    preferred_provider=LLMProvider.ANTHROPIC,
    required_capabilities=["text"]
)

if selected_model:
    # Create specific client
    client = create_client(
        provider=selected_model["provider"],
        model=selected_model["name"]
    )
    
    # Use client directly
    from llamasearch_experimentalagents_product_growth.core.llm_client import LLMMessage
    
    response = client.complete(
        messages=[
            LLMMessage.system("You are a creative writer."),
            LLMMessage.user("Write a short poem about AI.")
        ],
        temperature=0.9
    )
    
    print(response.content)
```

## Error Handling

```python
try:
    response = complete_prompt(
        prompt="Your prompt",
        provider="openai"
    )
except ValueError as e:
    # Configuration errors (missing API keys, etc.)
    print(f"Configuration error: {e}")
except Exception as e:
    # API errors, rate limits, etc.
    print(f"Error calling LLM: {e}")
    # Implement fallback mechanisms
```

## Next Steps

Now that you understand how to use the LLM Router, you can:

1. Try different LLM providers to compare results
2. Experiment with different temperature settings
3. Implement fallback mechanisms for production use
4. Use function calling for more structured outputs 