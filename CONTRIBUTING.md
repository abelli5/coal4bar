# Contributing to coal4bar

Thank you for your interest in contributing to coal4bar! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help each other learn and grow

## How to Contribute

### Reporting Bugs

Before submitting a bug report, check the issue list to avoid duplicates.

Include:
- Python version
- coal4bar version
- Operating system
- Detailed steps to reproduce
- Expected vs actual behavior
- Code sample if applicable

### Suggesting Features

Describe:
- Use case and motivation
- Implementation ideas (if you have them)
- Potential impact and benefits

### Submitting Pull Requests

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** with clear commit messages
4. **Write/update tests** for new functionality
5. **Update documentation** as needed
6. **Ensure code quality**:
   ```bash
   black coal4bar tests examples
   flake8 coal4bar tests examples
   mypy coal4bar
   pytest tests/
   ```
7. **Push** to your fork and **submit a Pull Request**

## Development Setup

```bash
# Clone repository
git clone https://github.com/abelli5/coal4bar.git
cd coal4bar

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8
- Use `black` for formatting
- Use meaningful variable names
- Add docstrings to functions and classes

## Testing

- Write tests for new features
- Ensure existing tests pass
- Target >80% code coverage

```bash
pytest tests/ -v --cov=coal4bar
```

## Documentation

- Update docstrings for code changes
- Update README.md for user-facing changes
- Keep PHYSICS_AND_THEORY.md current with significant algorithm changes

## Commit Messages

- Be descriptive and concise
- Use imperative mood ("Add feature" not "Added feature")
- Reference issues when relevant: "Fix #123"

## Questions?

- Open a discussion on GitHub
- Check existing documentation and issues

Thank you for contributing! 🎉
