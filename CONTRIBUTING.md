# Contributing to OpenClaw Self-Learning Suite

Thank you for your interest in contributing to the OpenClaw Self-Learning Suite! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- 🐛 **Report Bugs** - Open an issue with bug details
- 💡 **Suggest Features** - Share your ideas for improvement
- 📝 **Improve Documentation** - Fix typos, clarify explanations
- 🔧 **Submit Code** - Fix bugs or implement new features
- 🧪 **Add Tests** - Improve test coverage

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/openclaw-self-learning-suite.git
   cd openclaw-self-learning-suite
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## 📋 Development Guidelines

### Code Style

We use:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black openclaw_self_learning

# Check linting
flake8 openclaw_self_learning

# Type checking
mypy openclaw_self_learning
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for >80% code coverage

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=openclaw_self_learning

# Run specific test
pytest tests/test_plan_mode.py
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add new strategy selection algorithm
fix: resolve memory leak in review system
docs: update API documentation
test: add tests for collective intelligence
refactor: simplify plan generation logic
```

## 🔄 Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run checks**
   ```bash
   black openclaw_self_learning
   flake8 openclaw_self_learning
   pytest
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add my new feature"
   git push origin feature/my-new-feature
   ```

5. **Create Pull Request**
   - Describe what you changed and why
   - Link related issues
   - Ensure CI checks pass

## 📁 Project Structure

```
openclaw-self-learning-suite/
├── openclaw_self_learning/     # Main package
│   ├── __init__.py
│   ├── agent.py               # Self-learning agent
│   ├── skill_mixin.py         # OpenClaw integration
│   ├── config.py              # Configuration
│   └── systems/               # Six learning systems
│       ├── plan_mode.py
│       ├── auto_review.py
│       ├── nudge.py
│       ├── skill_evolution.py
│       ├── meta_learning.py
│       └── collective_intelligence.py
├── tests/                      # Test files
├── examples/                   # Usage examples
├── docs/                       # Documentation
└── README.md
```

## 🎨 Code Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions focused

Example:
```python
def process_task(
    user_input: str,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process user task with learning systems.
    
    Args:
        user_input: User's input message
        session_id: Optional session identifier
        
    Returns:
        Response dictionary with results
    """
    # Implementation
    pass
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to public APIs
- Include examples for new features
- Update CHANGELOG.md

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description** - What happened?
2. **Steps to reproduce** - How can we recreate it?
3. **Expected behavior** - What should have happened?
4. **Environment** - Python version, OS, etc.
5. **Logs** - Relevant error messages

## 💡 Suggesting Features

Feature requests are welcome! Please:

1. Check if already suggested
2. Describe the use case
3. Explain why it would be useful
4. Consider implementation approach

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different viewpoints

## 📞 Questions?

- 💬 Join our [Discord](https://discord.gg/openclaw)
- 📧 Email: community@openclaw.dev
- 🐦 Twitter: @OpenClawAI

Thank you for contributing! 🎉
