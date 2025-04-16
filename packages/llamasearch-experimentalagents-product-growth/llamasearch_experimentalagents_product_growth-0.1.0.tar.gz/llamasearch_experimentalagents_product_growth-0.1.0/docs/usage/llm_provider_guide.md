# LLM Provider Guide

This guide explains how to configure and use different Large Language Model (LLM) providers with LlamaSearch Experimental Agents: Product Growth.

## Table of Contents
- [Supported Providers](#supported-providers)
- [Configuration](#configuration)
- [Provider Selection](#provider-selection)
- [Provider-Specific Settings](#provider-specific-settings)
- [Performance Considerations](#performance-considerations)
- [Cost Management](#cost-management)
- [Troubleshooting](#troubleshooting)

## Supported Providers

LlamaSearch currently supports the following LLM providers:

1. **OpenAI**: Default provider, offering models like GPT-4, GPT-3.5-Turbo.
2. **Anthropic**: Provider of Claude models, known for long context windows.
3. **Hugging Face**: For open-source models.
4. **Custom Providers**: Support for custom or self-hosted models.

## Configuration

### API Keys

Before using any provider, you need to set up the appropriate API keys as environment variables:

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Hugging Face
export HUGGINGFACE_API_TOKEN="your-huggingface-token"
```

You can also use a `.env` file in your project root:

```
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
HUGGINGFACE_API_TOKEN=your-huggingface-token
```

Then, load these variables in your application:

```python
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env
```

## Provider Selection

### Command Line

When using the CLI, you can specify the provider with the `--provider` flag:

```bash
# Using OpenAI (default)
llamasearch analyze-feedback --input feedback.csv --provider openai

# Using Anthropic
llamasearch analyze-feedback --input feedback.csv --provider anthropic

# Using Hugging Face
llamasearch analyze-feedback --input feedback.csv --provider huggingface
```

### In Python Code

When using the library in your Python code, you can specify the provider using the `LLMProvider` enum:

```python
from llamasearch_experimentalagents_product_growth.core import analyze_text
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMProvider

# Using OpenAI
results_openai = analyze_text(
    text=["Your feedback text here"],
    analysis_type="sentiment_themes",
    provider=LLMProvider.OPENAI  # This is the default if omitted
)

# Using Anthropic
results_anthropic = analyze_text(
    text=["Your feedback text here"],
    analysis_type="sentiment_themes",
    provider=LLMProvider.ANTHROPIC
)

# Using Hugging Face
results_hf = analyze_text(
    text=["Your feedback text here"],
    analysis_type="sentiment_themes",
    provider=LLMProvider.HUGGINGFACE
)
```

### Default Provider Configuration

You can set a default provider in your configuration file:

```bash
# Create or edit the config file
llamasearch config set default_provider anthropic
```

Or modify the config file directly at `~/.llamasearch/config.json`:

```json
{
  "default_provider": "anthropic",
  "openai": {
    "model": "gpt-4"
  },
  "anthropic": {
    "model": "claude-2"
  }
}
```

## Provider-Specific Settings

### OpenAI Settings

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMRouter, LLMProvider, OpenAIConfig

# Configure OpenAI settings
openai_config = OpenAIConfig(
    model="gpt-4",
    temperature=0.3,
    max_tokens=1000,
    top_p=0.95
)

# Create a router with this configuration
router = LLMRouter(provider=LLMProvider.OPENAI, openai_config=openai_config)

# Use the router for text completion
response = router.complete_prompt("Analyze this customer feedback: ...")
```

Configuration options for OpenAI:

| Parameter | Description | Default |
|-----------|-------------|---------|
| model | Model to use (e.g., "gpt-4", "gpt-3.5-turbo") | "gpt-4" |
| temperature | Controls randomness (0.0 to 1.0) | 0.7 |
| max_tokens | Maximum tokens to generate | 1000 |
| top_p | Nucleus sampling parameter | 1.0 |
| frequency_penalty | Penalty for token frequency | 0.0 |
| presence_penalty | Penalty for token presence | 0.0 |

### Anthropic Settings

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMRouter, LLMProvider, AnthropicConfig

# Configure Anthropic settings
anthropic_config = AnthropicConfig(
    model="claude-2",
    temperature=0.5,
    max_tokens_to_sample=2000
)

# Create a router with this configuration
router = LLMRouter(provider=LLMProvider.ANTHROPIC, anthropic_config=anthropic_config)

# Use the router for text completion
response = router.complete_prompt("Analyze this customer feedback: ...")
```

Configuration options for Anthropic:

| Parameter | Description | Default |
|-----------|-------------|---------|
| model | Model to use (e.g., "claude-2", "claude-instant-1") | "claude-2" |
| temperature | Controls randomness (0.0 to 1.0) | 0.7 |
| max_tokens_to_sample | Maximum tokens to generate | 2000 |
| top_p | Nucleus sampling parameter | 1.0 |
| top_k | Top-k filtering parameter | -1 (disabled) |

### Hugging Face Settings

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMRouter, LLMProvider, HuggingFaceConfig

# Configure Hugging Face settings
hf_config = HuggingFaceConfig(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    max_length=512,
    temperature=0.7
)

# Create a router with this configuration
router = LLMRouter(provider=LLMProvider.HUGGINGFACE, huggingface_config=hf_config)

# Use the router for text completion
response = router.complete_prompt("Analyze this customer feedback: ...")
```

Configuration options for Hugging Face:

| Parameter | Description | Default |
|-----------|-------------|---------|
| model | Model identifier on Hugging Face | "mistralai/Mistral-7B-Instruct-v0.1" |
| max_length | Maximum sequence length | 512 |
| temperature | Controls randomness (0.0 to 1.0) | 0.7 |
| top_p | Nucleus sampling parameter | 0.95 |
| top_k | Top-k filtering parameter | 50 |

## Performance Considerations

Each provider has different strengths and weaknesses:

### OpenAI (GPT Models)
- **Strengths**: High-quality responses, good for most general tasks
- **Weaknesses**: Can be more expensive, shorter context windows in some models

### Anthropic (Claude Models)
- **Strengths**: Very large context windows (up to 100,000 tokens), good instruction following
- **Weaknesses**: May be slower for some tasks

### Hugging Face Models
- **Strengths**: Many open-source options, can be run locally
- **Weaknesses**: Quality may vary, setup can be more complex

### Choosing the Right Provider

Consider these factors when selecting a provider:

1. **Task Complexity**: For complex analysis, GPT-4 or Claude-2 often perform best
2. **Context Length**: For analyzing large documents, Claude models excel
3. **Speed Requirements**: For real-time applications, smaller models like GPT-3.5-Turbo may be faster
4. **Cost Sensitivity**: Open-source models can reduce costs significantly
5. **Data Privacy**: Self-hosted models offer maximum privacy control

## Cost Management

Different providers have different pricing structures. Here are some tips to optimize costs:

1. **Model Selection**: Choose smaller models for simpler tasks
   ```python
   # Use a smaller model for basic sentiment analysis
   router = LLMRouter(
       provider=LLMProvider.OPENAI, 
       openai_config=OpenAIConfig(model="gpt-3.5-turbo")
   )
   ```

2. **Token Usage**: Monitor and optimize your prompts to use fewer tokens
   ```python
   # Instead of this
   long_prompt = "Analyze the following customer feedback in great detail, considering all aspects of..."
   
   # Use a more concise prompt
   efficient_prompt = "Analyze customer feedback, identify key themes and sentiment:"
   ```

3. **Batching**: Batch multiple requests when possible
   ```python
   # Process multiple feedback items at once instead of one by one
   batch_results = analyze_text(
       text=["Feedback 1", "Feedback 2", "Feedback 3"],
       analysis_type="sentiment_themes"
   )
   ```

4. **Caching**: Implement caching for repeated or similar queries
   ```python
   import hashlib
   import json
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_analysis(text_hash):
       # Retrieve cached result or perform analysis
       pass
   
   def analyze_with_cache(text):
       # Create a hash of the input
       text_hash = hashlib.md5(text.encode()).hexdigest()
       return cached_analysis(text_hash)
   ```

## Troubleshooting

### Common Issues

#### API Key Issues
```
Error: Authentication error with [Provider]
```

**Solution**: Check that your API key is correctly set in the environment variables or .env file.

#### Rate Limiting
```
Error: Rate limit exceeded for [Provider]
```

**Solution**: Implement exponential backoff or reduce the number of concurrent requests.

```python
import time
import random

def call_with_retry(func, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            if "rate limit" in str(e).lower():
                wait_time = (2 ** retries) + random.uniform(0, 1)
                print(f"Rate limited, waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                raise
    raise Exception("Max retries exceeded")
```

#### Model Not Available
```
Error: Model [model_name] not found
```

**Solution**: Check that you're using a valid model name for the selected provider.

### Debugging Provider Selection

To verify which provider is being used:

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMRouter, LLMProvider

# Create router with explicit provider
router = LLMRouter(provider=LLMProvider.OPENAI)

# Check active provider
print(f"Active provider: {router.provider.name}")

# Check active model
print(f"Active model: {router.get_active_model()}")
```

### Logging

Enable detailed logging to troubleshoot provider issues:

```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("llamasearch.llm_router")
logger.setLevel(logging.DEBUG)

# Now your LLM router calls will produce detailed logs
```

## Advanced: Custom Provider Integration

For advanced users, you can integrate custom LLM providers:

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMRouter, LLMProvider, BaseProviderConfig

# Create a custom provider configuration
class CustomProviderConfig(BaseProviderConfig):
    def __init__(self, endpoint_url, api_key, model="custom-model"):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.model = model

# Extend the LLMRouter to support your custom provider
class CustomLLMRouter(LLMRouter):
    def __init__(self, custom_config):
        self.custom_config = custom_config
        super().__init__(provider=LLMProvider.CUSTOM)
        
    def complete_prompt(self, prompt, **kwargs):
        # Implement your custom API call here
        # Example:
        import requests
        response = requests.post(
            self.custom_config.endpoint_url,
            headers={"Authorization": f"Bearer {self.custom_config.api_key}"},
            json={
                "prompt": prompt,
                "model": self.custom_config.model,
                **kwargs
            }
        )
        return response.json()["completion"]
```

For more details on integrating custom providers, please refer to the [Developer Documentation](developer_docs.md). 