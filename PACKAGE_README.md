# OpenClaw Self-Learning Suite - GitHub Package

## 📦 Package Overview

This is a production-ready Python package that integrates all six self-learning systems into a cohesive, easy-to-use suite for OpenClaw agents.

### 🎯 What's Included

```
openclaw-self-learning-suite/
├── openclaw_self_learning/           # Main package
│   ├── __init__.py                  # Package exports
│   ├── agent.py                     # SelfLearningAgent class
│   ├── skill_mixin.py               # OpenClaw integration mixin
│   ├── config.py                    # Configuration management
│   ├── cli.py                       # Command-line interface
│   └── systems/                     # Six learning systems
│       ├── plan_mode.py
│       ├── auto_review.py
│       ├── nudge.py
│       ├── skill_evolution.py
│       ├── meta_learning.py
│       └── collective_intelligence.py
├── tests/                            # Test suite
├── examples/                         # Usage examples
├── docs/                             # Documentation
├── setup.py                          # Package setup
├── requirements.txt                  # Dependencies
├── requirements-dev.txt              # Dev dependencies
├── LICENSE                           # MIT License
├── README.md                         # Main README
└── CONTRIBUTING.md                   # Contribution guide
```

## 🚀 Quick Start

### Installation

```bash
# From source (recommended during development)
git clone https://github.com/yourusername/openclaw-self-learning-suite.git
cd openclaw-self-learning-suite
pip install -e .

# Or install from PyPI (when published)
pip install openclaw-self-learning-suite
```

### Basic Usage

```python
from openclaw_self_learning import SelfLearningAgent

# Create agent
agent = SelfLearningAgent(
    agent_id="my-agent",
    user_id="user-001",
    name="My Learning Agent"
)

# Use agent - all six systems engage automatically
response = agent.process("Help me with this task")
print(response['content'])
```

### OpenClaw Skill Integration

```python
from openclaw_self_learning import SelfLearningSkillMixin

class MySmartSkill(SelfLearningSkillMixin):
    def __init__(self):
        super().__init__()
        self.init_self_learning(
            agent_id="my-skill",
            user_id="user-001",
            agent_name="My Smart Skill"
        )
    
    def run(self, session_id, user_input):
        return self.process_with_learning(session_id, user_input)
```

## 🔧 CLI Commands

```bash
# Initialize configuration
openclaw-self-learning init

# Check system status
openclaw-self-learning status

# Run tests
openclaw-self-learning test

# Run examples
openclaw-self-learning example basic
openclaw-self-learning example skill
```

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=openclaw_self_learning

# Run specific test
pytest tests/test_basic.py::TestSelfLearningAgent
```

## 📁 Integration with Full Systems

This package provides lightweight wrappers that:
1. **Try to import** from the full implementation systems (if available)
2. **Fallback to minimal implementations** if full systems aren't installed

### Full Systems Location

The complete implementations are in:
```
/workspace/projects/workspace/01-projects/
├── plan-mode/
├── auto-review-system/
├── skill-evolution-system/
├── meta-learning-system/
├── collective-intelligence-system/
└── nudge-system-prototype/
```

To use full implementations:
```bash
# Clone this repo alongside the full systems
cd /workspace/projects/workspace/01-projects/
git clone https://github.com/yourusername/openclaw-self-learning-suite.git

# The package will automatically detect and use full systems
```

## 📦 Publishing to PyPI

### Preparation

1. **Update version** in `setup.py`:
   ```python
   version="1.0.0",
   ```

2. **Build distribution**:
   ```bash
   python setup.py sdist bdist_wheel
   ```

3. **Test with TestPyPI**:
   ```bash
   twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

4. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

### Automated Publishing (GitHub Actions)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools wheel twine
    - name: Build and publish
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        python setup.py sdist bdist_wheel
        twine upload dist/*
```

## 🌟 Features

- ✅ **Six Integrated Learning Systems**
- ✅ **OpenClaw Skill Mixin** - Easy integration
- ✅ **Configuration Management** - YAML-based config
- ✅ **CLI Interface** - Command-line tools
- ✅ **Comprehensive Tests** - pytest suite
- ✅ **Documentation** - Installation, API, examples
- ✅ **MIT Licensed** - Open source

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-04-09 | Initial release with all six systems |

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📞 Support

- 📖 [Documentation](docs/)
- 💬 [Discord](https://discord.gg/openclaw)
- 🐛 [GitHub Issues](https://github.com/yourusername/openclaw-self-learning-suite/issues)

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

---

**Built with ❤️ for the OpenClaw Community**
