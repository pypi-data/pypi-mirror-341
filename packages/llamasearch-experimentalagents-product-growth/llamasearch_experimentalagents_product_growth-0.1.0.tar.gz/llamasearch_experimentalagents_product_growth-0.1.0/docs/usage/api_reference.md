# API Reference

This document provides detailed reference information for the core modules and functions in the LlamaSearch Experimental Agents Product Growth package.

## Core Module

### LLM Router

```python
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMRouter, LLMProvider
```

#### Classes

**`LLMRouter`**

Main router class for managing LLM providers and model selection.

```python
router = LLMRouter(config: Optional[Dict[str, Any]] = None)
```

Parameters:
- `config`: Optional dictionary with configuration options. If not provided, configuration is loaded from environment variables.

Methods:
- `get_available_models() -> List[Dict[str, Any]]`: Returns list of available models across all configured providers.
- `select_model(task: str, preferred_provider: Optional[LLMProvider] = None, required_capabilities: Optional[List[str]] = None) -> Optional[Dict[str, Any]]`: Selects best model for a task.
- `get_client(provider: Union[str, LLMProvider], model: Optional[str] = None) -> LLMClient`: Returns an LLM client for specified provider and model.

**`LLMProvider`**

Enum representing supported LLM providers.

```python
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    # Additional providers...
```

#### Functions

**`get_available_models(providers: Optional[List[Union[str, LLMProvider]]] = None) -> List[Dict[str, Any]]`**

Get available models across specified providers.

Parameters:
- `providers`: Optional list of providers to check. If not provided, checks all configured providers.

Returns:
- List of dictionaries with model information.

### LLM Client

```python
from llamasearch_experimentalagents_product_growth.core.llm_client import (
    LLMClient, OpenAIClient, AnthropicClient, LocalClient, create_client, LLMMessage, LLMFunction
)
```

#### Classes

**`LLMClient`**

Abstract base class for LLM provider clients.

Methods:
- `complete(messages: List[LLMMessage], temperature: float = 0.7, max_tokens: Optional[int] = None, functions: Optional[List[LLMFunction]] = None) -> LLMResponse`: Completes a conversation with the LLM.

**`LLMMessage`**

Class representing a message in an LLM conversation.

```python
# Static creation methods
LLMMessage.system(content: str) -> LLMMessage
LLMMessage.user(content: str) -> LLMMessage
LLMMessage.assistant(content: str, function_call: Optional[Dict[str, Any]] = None) -> LLMMessage
LLMMessage.function(name: str, content: str) -> LLMMessage
```

**`LLMFunction`**

Class representing a function that can be called by the LLM.

```python
function = LLMFunction(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    required: Optional[List[str]] = None
)
```

**`LLMResponse`**

Class representing a response from an LLM.

Properties:
- `content`: The response text
- `function_call`: Optional dictionary with function call information
- `provider`: The provider that generated the response
- `model`: The model that generated the response
- `usage`: Token usage information

#### Functions

**`create_client(provider: Union[str, LLMProvider], model: Optional[str] = None, **kwargs) -> LLMClient`**

Factory function for creating an appropriate LLM client.

Parameters:
- `provider`: Provider enum or string
- `model`: Optional model name
- `**kwargs`: Additional parameters passed to the client constructor

Returns:
- An instance of the appropriate LLMClient subclass

### LLM Utilities

```python
from llamasearch_experimentalagents_product_growth.core import (
    complete_prompt, chat_completion, analyze_text, generate_strategies
)
```

#### Functions

**`complete_prompt(prompt: str, system_prompt: Optional[str] = None, provider: Optional[Union[str, LLMProvider]] = None, model: Optional[str] = None, temperature: float = 0.7, max_tokens: Optional[int] = None) -> str`**

High-level function for generating completions from a prompt.

Parameters:
- `prompt`: User prompt text
- `system_prompt`: Optional system instruction
- `provider`: Optional provider to use
- `model`: Optional model to use
- `temperature`: Controls randomness (0.0-1.0)
- `max_tokens`: Maximum response length

Returns:
- Generated text response

**`chat_completion(messages: List[LLMMessage], provider: Optional[Union[str, LLMProvider]] = None, model: Optional[str] = None, temperature: float = 0.7, max_tokens: Optional[int] = None, functions: Optional[List[LLMFunction]] = None) -> LLMResponse`**

Generate a completion from a conversation history.

Parameters:
- `messages`: List of LLMMessage objects representing the conversation
- `provider`: Optional provider to use
- `model`: Optional model to use
- `temperature`: Controls randomness (0.0-1.0)
- `max_tokens`: Maximum response length
- `functions`: Optional list of functions the model can call

Returns:
- LLMResponse object with the completion and metadata

**`analyze_text(text: str, analysis_type: str, provider: Optional[Union[str, LLMProvider]] = None, model: Optional[str] = None) -> Dict[str, Any]`**

Analyze text for sentiment, themes, summarization, etc.

Parameters:
- `text`: Text to analyze
- `analysis_type`: Type of analysis ("sentiment", "themes", "summary", etc.)
- `provider`: Optional provider to use
- `model`: Optional model to use

Returns:
- Dictionary with analysis results

**`generate_strategies(feedback_analysis: Dict[str, Any], max_strategies: int = 5, provider: Optional[Union[str, LLMProvider]] = None, model: Optional[str] = None) -> List[Dict[str, Any]]`**

Generate product growth strategies from feedback analysis.

Parameters:
- `feedback_analysis`: Dictionary with feedback analysis data
- `max_strategies`: Maximum number of strategies to generate
- `provider`: Optional provider to use
- `model`: Optional model to use

Returns:
- List of dictionaries with growth strategy recommendations

## Strategy Module

```python
from llamasearch_experimentalagents_product_growth.strategy import (
    Priority, GTMStrategy, GrowthRecommendation, StrategicRoadmap
)
```

#### Classes

**`Priority`**

Enum representing priority levels.

```python
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

**`GTMStrategy`**

Enum representing go-to-market strategies.

```python
class GTMStrategy(str, Enum):
    PRODUCT_LED = "product_led"
    SALES_LED = "sales_led"
    MARKETING_LED = "marketing_led"
    COMMUNITY_LED = "community_led"
```

**`GrowthRecommendation`**

Pydantic model for a growth recommendation.

```python
class GrowthRecommendation(BaseModel):
    feature: str
    rationale: str
    priority: Priority
    expected_impact: str
    implementation_cost: str
    gtm_strategies: List[GTMStrategy]
```

**`StrategicRoadmap`**

Pydantic model for a strategic roadmap.

```python
class StrategicRoadmap(BaseModel):
    recommendations: List[GrowthRecommendation]
    executive_summary: str
    market_context: str
    implementation_timeline: str
```

## CLI Module

```python
from llamasearch_experimentalagents_product_growth.cli import app
```

Command-line interface for the package.

Commands:
- `llamasearch feedback analyze`: Analyze customer feedback
- `llamasearch strategize`: Generate growth strategies
- `llamasearch llm complete`: Generate completions
- `llamasearch llm chat`: Interactive chat with an LLM
- `llamasearch llm models`: List available LLM models

## Analysis Module

```python
from llamasearch_experimentalagents_product_growth.analysis import analyze_feedback
```

#### Functions

**`analyze_feedback(feedback_data: Union[str, List[str], pd.DataFrame], columns: Optional[Dict[str, str]] = None, methods: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]`**

Analyze customer feedback data.

Parameters:
- `feedback_data`: Feedback data as string, list, or DataFrame
- `columns`: Optional mapping of column names
- `methods`: Optional list of analysis methods to apply
- `**kwargs`: Additional parameters for analysis methods

Returns:
- Dictionary with analysis results

## Environment Configuration

Environment variables for configuration:

- `OPENAI_API_KEY`: API key for OpenAI
- `ANTHROPIC_API_KEY`: API key for Anthropic
- `LLM_PROVIDERS`: Comma-separated list of enabled providers
- `LLM_DEFAULT_PROVIDER`: Default LLM provider
- `LLM_DEFAULT_MODEL`: Default model name
- `LLM_LOCAL_MODEL_PATH`: Path to local model files
- `LLM_TEMPERATURE`: Default temperature for completions
- `LLM_MAX_TOKENS`: Default maximum tokens for completions 