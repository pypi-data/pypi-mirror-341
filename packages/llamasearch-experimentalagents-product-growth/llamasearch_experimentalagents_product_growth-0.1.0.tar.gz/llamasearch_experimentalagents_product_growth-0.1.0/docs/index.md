# LlamaSearch ExperimentalAgents: Product Growth

<div align="center">
   <img src="images/logo.png" alt="LlamaSearch Logo" width="200"/>
</div>

## Overview

LlamaSearch ExperimentalAgents: Product Growth is a cutting-edge AI platform for analyzing customer feedback and generating data-driven growth strategies. It combines OpenAI's advanced agent architecture with hardware-accelerated NLP, retrieval-augmented generation, and immersive visualizations to help product teams make better decisions.

Built with performance and extensibility in mind, it leverages Rust extensions via PyO3 for computationally intensive operations and MLX acceleration on Apple Silicon, while providing a beautiful cross-platform GUI through Tauri.

## Key Features

### 🤖 Advanced AI Agents

- **Multi-Agent Orchestration**: Specialized agents work together to analyze feedback and generate strategies
- **Function-Calling**: Agents call tools and functions to perform complex tasks
- **Structured Outputs**: JSON schema enforcement ensures consistent, parseable responses

### 🧠 Hardware-Accelerated NLP

- **MLX Optimization**: Leverages Apple's MLX framework for blazing-fast performance on Apple Silicon
- **JAX Support**: Optimized with JAX for GPU acceleration on supported platforms
- **Adaptive Backend**: Automatically selects the fastest backend based on available hardware

### 📚 RAG Knowledge Enhancement

- **Semantic Search**: Find relevant information with vector embeddings
- **Context-Aware Responses**: Generate more accurate strategies by retrieving and incorporating relevant data
- **Multiple Vector Store Options**: Support for SQLite, FAISS, and other vector databases

### 🔀 Multi-LLM Strategy

- **Provider Fallback**: Automatically switch between OpenAI, Anthropic, and local models
- **Local Models**: Run models locally with MLX acceleration on macOS
- **Cost Optimization**: Use the right model for each task based on complexity and budget

### 💾 SQLite-based Memory & Logging

- **Persistent Agent Memory**: Store and recall past interactions and insights
- **Comprehensive Logging**: Track all agent actions and decisions
- **Datasette Integration**: Explore logs and memory through an intuitive web interface

### ⚡ Rust Performance

- **PyO3 Extensions**: Critical pathways optimized in Rust
- **Cross-Platform Binaries**: Pre-built wheels for all major platforms
- **Memory Safety**: Leverage Rust's safety guarantees for robust code

### 🖥️ Tauri v2 GUI

- **Modern Interface**: Clean, intuitive UI built with Next.js
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Vision Pro-Inspired Design**: Beautiful glassmorphic UI components

## Getting Started

Follow our [Quick Start Guide](quickstart.md) to begin using LlamaSearch ExperimentalAgents: Product Growth in minutes.

```bash
# Install the package
pip install llamasearch-experimentalagents-product-growth

# Set your API key
export OPENAI_API_KEY=your-api-key

# Analyze customer feedback
llamasearch-growth analyze --feedback data.csv --output-dir ./insights
```

## Examples

Check out these examples to see what LlamaSearch ExperimentalAgents: Product Growth can do:

- [Analyzing Customer Feedback](examples.md#analyzing-customer-feedback)
- [Generating Growth Strategies](examples.md#generating-growth-strategies)
- [Creating Visualizations](examples.md#creating-visualizations)
- [Using the GUI](examples.md#using-the-gui)

## Who is LlamaSearch for?

- **Product Managers**: Get actionable insights from customer feedback
- **Growth Teams**: Identify opportunities and prioritize initiatives
- **UX Researchers**: Analyze user feedback at scale
- **Developers**: Integrate advanced AI capabilities into your workflow

## Next Steps

- [Installation Guide](installation.md): Detailed installation instructions
- [Configuration](configuration.md): Configure the library for your needs
- [API Reference](api/agents.md): Explore the API documentation
- [Advanced Topics](advanced/openai-agents.md): Dive deeper into advanced features 