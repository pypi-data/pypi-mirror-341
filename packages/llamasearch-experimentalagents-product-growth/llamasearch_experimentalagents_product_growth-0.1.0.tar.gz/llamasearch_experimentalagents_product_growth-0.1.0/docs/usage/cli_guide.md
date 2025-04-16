# Command-Line Interface Guide

LlamaSearch Experimental Agents provides a powerful command-line interface (CLI) for running various product growth tasks without writing code. This guide explains how to use the CLI effectively.

## Installation

Make sure you have installed the package with all required dependencies:

```bash
pip install -e ".[all]"
```

## Basic Usage

The CLI can be accessed using the `llamasearch` command:

```bash
llamasearch --help
```

This will display all available commands and options.

## Environment Setup

Before using the CLI, set up your environment with the necessary API keys:

```bash
# Create a .env file from the template
cp .env.example .env

# Edit the .env file with your API keys
# OPENAI_API_KEY=your-key-here
# ANTHROPIC_API_KEY=your-key-here
```

## Analyzing Customer Feedback

Analyze customer feedback from a CSV file:

```bash
llamasearch feedback analyze path/to/feedback.csv \
  --text-column "feedback_text" \
  --sentiment-column "sentiment" \
  --output "analysis_results.json"
```

Options:
- `--text-column`: Column containing the feedback text (default: "text")
- `--sentiment-column`: Column containing sentiment values, if available (default: none)
- `--output`: Path to save the analysis results (default: stdout)
- `--cluster-count`: Number of clusters to create (default: auto-detect)
- `--provider`: LLM provider to use for analysis (default: auto-select)

## Generating Growth Strategies

Generate product growth strategies based on feedback analysis:

```bash
llamasearch strategize --input "analysis_results.json" \
  --output "strategic_roadmap.json" \
  --max-strategies 5 \
  --provider openai \
  --model gpt-4o
```

Options:
- `--input`: Path to the feedback analysis JSON file
- `--output`: Path to save the strategic roadmap (default: stdout)
- `--max-strategies`: Maximum number of strategies to generate (default: 5)
- `--provider`: LLM provider to use (default: auto-select)
- `--model`: Specific model to use (default: best available)

## LLM Commands

### List Available Models

List all available LLM models:

```bash
llamasearch llm models
```

You'll see output similar to:

```
Available LLM Models:
--------------------
gpt-4o (openai)
  Context: 128000 tokens
  Capabilities: text, vision, function_calling
  Hardware: OpenAI API

claude-3-sonnet (anthropic)
  Context: 200000 tokens
  Capabilities: text, vision
  Hardware: Anthropic API
  
...
```

### Generate Completions

Generate text completions directly from the command line:

```bash
llamasearch llm complete "Generate three product improvement ideas for a to-do app" \
  --system "You are a product growth expert." \
  --provider openai \
  --model gpt-4o \
  --temperature 0.7 \
  --max-tokens 500
```

Options:
- `--system`: System prompt/instructions (optional)
- `--provider`: LLM provider to use (default: auto-select)
- `--model`: Specific model to use (default: best available)
- `--temperature`: Controls randomness (0-1, default: 0.7)
- `--max-tokens`: Maximum response length (default: model-dependent)

### Interactive Chat

Start an interactive chat session with an LLM:

```bash
llamasearch llm chat --provider anthropic --model claude-3-sonnet
```

This opens an interactive session where you can have a conversation with the model. Type `exit` or `quit` to end the session.

## Exporting and Sharing Results

Export analysis results to different formats:

```bash
# Export to CSV
llamasearch feedback analyze path/to/feedback.csv --output results.csv --format csv

# Export to JSON (default)
llamasearch feedback analyze path/to/feedback.csv --output results.json

# Export strategic roadmap to PDF
llamasearch strategize --input results.json --output roadmap.pdf --format pdf
```

## Custom Configurations

You can create custom configuration profiles:

```bash
# Save a configuration profile
llamasearch config save my-profile \
  --provider openai \
  --model gpt-4o \
  --temperature 0.8

# Use a saved profile
llamasearch strategize --input results.json --profile my-profile
```

## Advanced Example: Complete Workflow

Here's an example of a complete workflow:

```bash
# Analyze feedback
llamasearch feedback analyze customer_feedback.csv \
  --text-column "comment" \
  --output feedback_analysis.json

# Generate strategies
llamasearch strategize \
  --input feedback_analysis.json \
  --output growth_strategy.json \
  --max-strategies 8 \
  --provider openai \
  --model gpt-4o

# Create a beautiful PDF report
llamasearch export growth_strategy.json \
  --format pdf \
  --template executive \
  --output strategic_roadmap.pdf
```

## Troubleshooting

If you encounter issues:

1. Check your API keys are correctly set in the `.env` file
2. Ensure you have the latest version installed: `pip install -U llamasearch-experimentalagents-product-growth`
3. Try with the `--verbose` flag to see detailed logs
4. For connectivity issues, try the `--timeout 60` parameter to increase request timeouts

For more help, run any command with the `--help` flag for detailed information about its options and arguments. 