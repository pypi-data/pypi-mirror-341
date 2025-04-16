# LlamaSearch ExperimentalAgents: Product Growth

![Build Status](https://img.shields.io/github/workflow/status/llamasearch/experimentalagents-product-growth/CI)
![Coverage](https://img.shields.io/codecov/c/github/llamasearch/experimentalagents-product-growth)
![Version](https://img.shields.io/pypi/v/llamasearch-experimentalagents-product-growth)
![License](https://img.shields.io/github/license/llamasearch/experimentalagents-product-growth)

A cutting-edge AI platform for analyzing customer feedback and generating data-driven growth strategies with multi-LLM support, MLX acceleration, and compelling visualizations.

## ✨ Features

- **Multi-LLM Router**: Seamlessly switch between OpenAI, Anthropic, and local models with automatic fallbacks
- **Hardware-Accelerated NLP**: Fast feedback analysis with MLX/JAX optimizations for Apple Silicon and other platforms
- **Strategy Generation**: AI-powered growth strategy recommendations with priority levels and GTM approaches
- **Engaging Visualizations**: Growth Garden and Insight Tree animations to present findings
- **Production Ready**: Comprehensive testing, CI/CD pipelines, and documentation

## 📦 Installation

```bash
# Install with pip
pip install llamasearch-experimentalagents-product-growth

# For development version
pip install git+https://github.com/llamasearch/experimentalagents-product-growth.git
```

For Apple Silicon users, MLX acceleration is available:

```bash
pip install 'llamasearch-experimentalagents-product-growth[mlx]'
```

## 🔧 Configuration

Create a `.env` file based on the example:

```bash
cp .env.example .env
```

Configure your LLM providers:

```
# API Keys
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Provider selection and fallback order
LLM_PROVIDERS=openai,anthropic,local
LLM_LOCAL_MODEL_PATH=/path/to/local/models
```

## 🚀 Quick Start

Analyze customer feedback and generate growth strategies:

```bash
# Analyze customer feedback
llamasearch analyze --feedback data.csv --output-dir ./insights

# Generate strategies using the multi-LLM router
llamasearch strategize --insights ./insights/analysis_results.json

# Visualize results
llamasearch visualize --data ./insights/strategies.json --type garden
```

## 🧠 LLM Router

The multi-LLM router enables seamless switching between different providers:

```python
from llamasearch_experimentalagents_product_growth.core import (
    complete_prompt, analyze_text, chat_completion
)

# Simple completion (auto-selects the best available model)
response = complete_prompt(
    prompt="Analyze the strengths of this feature: widgets with AI enhancement",
    system_prompt="You are a product strategist."
)

# Specify a provider
response = complete_prompt(
    prompt="Summarize this feedback",
    provider="anthropic",
    model="claude-3-haiku"
)

# Advanced chat completion
messages = [
    {"role": "system", "content": "You are a product strategist."},
    {"role": "user", "content": "How can we improve user onboarding?"}
]
response = chat_completion(
    messages=messages,
    temperature=0.7
)
```

## 📊 Example

Analyze customer feedback:

```python
from llamasearch_experimentalagents_product_growth.agents import analyze_feedback
import pandas as pd

# Load feedback data
feedback_df = pd.read_csv("customer_feedback.csv")

# Analyze feedback
results = analyze_feedback(
    feedback_df=feedback_df,
    text_column="comments",
    n_clusters=5,
    backend="auto"  # Automatically selects MLX on Apple Silicon
)

print(f"Identified {results['num_clusters']} feedback clusters")
print(f"Most positive cluster themes: {results['cluster_themes']['0']}")
```

Generate growth strategies:

```python
from llamasearch_experimentalagents_product_growth.agents import generate_growth_strategies

# Generate strategies based on feedback analysis
strategies = generate_growth_strategies(
    analysis_results=results,
    max_strategies=5,
    provider="openai",  # Use OpenAI models
    model="gpt-4o"  # Specify model (optional)
)

# Display strategies
for strategy in strategies:
    print(f"Strategy: {strategy.feature}")
    print(f"Priority: {strategy.priority}")
    print(f"GTM Approaches: {', '.join(strategy.gtm_strategies)}")
    print(f"Expected Impact: {strategy.expected_impact}")
    print("---")
```

## 📚 Documentation

Full documentation is available at [https://llamasearch.github.io/experimentalagents-product-growth](https://llamasearch.github.io/experimentalagents-product-growth)

## 🧪 Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=llamasearch_experimentalagents_product_growth
```

## 🤝 Contributing

Contributions are welcome! Please check out our [contribution guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 