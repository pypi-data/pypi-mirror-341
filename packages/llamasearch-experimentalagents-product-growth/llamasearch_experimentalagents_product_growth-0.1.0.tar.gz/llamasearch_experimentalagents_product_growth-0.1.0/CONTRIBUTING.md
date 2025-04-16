# Contributing to LlamaSearch ExperimentalAgents: Product Growth

Thank you for your interest in contributing to our project! This document provides guidelines for contributions and explains our development process.

## Code of Conduct

By participating in this project, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### 1. Setup your development environment

1. Fork the repository on GitHub
2. Clone your fork locally
```bash
git clone https://github.com/YOUR-USERNAME/experimentalagents-product-growth.git
cd experimentalagents-product-growth
```
3. Install the package in development mode
```bash
pip install -e ".[dev]"
```
4. Install pre-commit hooks
```bash
pre-commit install
```

### 2. Create a new branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Development Guidelines

- Follow the existing code style (we use Black and isort for formatting)
- Add or update tests for any new functionality
- Keep pull requests focused on a single topic
- Update documentation for any changed functionality

#### Code Style

We use several tools to ensure code quality:

- **Black**: For code formatting
- **isort**: For import sorting
- **mypy**: For type checking
- **ruff**: For linting

You can run these tools with:
```bash
black src tests
isort src tests
mypy src
ruff src tests
```

Or use the pre-commit hooks which will run automatically on commit:
```bash
pre-commit run --all-files
```

### 4. Test your changes

```bash
pytest
```

For more comprehensive testing:
```bash
pytest --cov=llamasearch_experimentalagents_product_growth
```

### 5. Commit and push your changes

```bash
git add .
git commit -m "Description of your changes"
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

Go to the repository on GitHub and create a new Pull Request from your feature branch.

In your PR description:
- Explain what the PR does
- Link to any relevant issues
- Note any breaking changes
- Include screenshots for UI changes

## Pull Request Process

1. Ensure your code passes all tests and checks
2. Update documentation as needed
3. Your PR needs to be approved by at least one maintainer
4. Once approved, a maintainer will merge your PR

## Adding New Dependencies

If you need to add a new dependency:
1. Add it to the appropriate section in `pyproject.toml`
2. Explain why it's needed in your PR description

## Working with the LLM Router

When modifying the LLM router:
1. Ensure all providers (OpenAI, Anthropic, local) are well supported
2. Maintain the fallback mechanism to ensure degraded functionality
3. Add tests for any new provider integrations
4. Document configuration options in the README

## Release Process

Our release process is managed by the maintainers:

1. Version bump in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. GitHub Actions will publish to PyPI

## Questions?

If you have any questions about contributing, please open an issue on GitHub with the label 'question'. 