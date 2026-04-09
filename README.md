# OpenClaw Self-Learning Suite

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green.svg)]()

> 🧠 **The Ultimate Self-Learning Ecosystem for AI Agents**

A comprehensive, production-ready skill suite that transforms your OpenClaw agent into a continuously self-improving AI with six integrated learning systems.

## 🌟 Features

### Six Integrated Learning Systems

| System | Status | Description |
|--------|--------|-------------|
| **Plan Mode** | ✅ | Pre-execution planning with user confirmation |
| **Auto-Review** | ✅ | Post-execution analysis and lesson extraction |
| **Nudge System** | ✅ | Periodic reminders to save knowledge |
| **Skill Evolution** | ✅ | Automatic skill optimization and versioning |
| **Meta-Learning** | ✅ | Strategy selection and evolution |
| **Collective Intelligence** | ✅ | Multi-agent knowledge sharing |

### Key Capabilities

- 🎯 **Intelligent Planning** - Automatic task breakdown with risk assessment
- 🔄 **Continuous Learning** - Every interaction improves future performance
- 📊 **Performance Tracking** - Monitor and optimize skill effectiveness
- 🧬 **Genetic Evolution** - Strategies evolve using genetic algorithms
- 🤝 **Knowledge Sharing** - Share and discover skills across agents
- 🔒 **Privacy First** - Configurable sharing modes and permissions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Snowayai/openclaw-self-learning-skill.git

# Install dependencies
pip install -r requirements.txt

# Install as OpenClaw skill
openclaw skill install ./openclaw-self-learning-skill
```

### Basic Usage

```python
from openclaw_self_learning import SelfLearningAgent

# Create a self-learning agent
agent = SelfLearningAgent(
    agent_id="my-agent",
    user_id="user-001",
    name="My Learning Agent"
)

# Use the agent - learning happens automatically
response = agent.process("Help me analyze this log file")
```

### OpenClaw Integration

```python
from openclaw_self_learning import SelfLearningSkillMixin

class MySkill(SelfLearningSkillMixin):
    def __init__(self):
        super().__init__()
        self.init_self_learning(
            agent_id="my-skill",
            user_id="user-001",
            agent_name="My Smart Skill"
        )
    
    def run(self, session_id, user_input):
        # All learning systems are automatically engaged
        return self.process_with_learning(session_id, user_input)
```

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Contributing](CONTRIBUTING.md)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Self-Learning Ecosystem                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User Input                                                   │
│      ↓                                                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  Plan Mode   │ →  │Meta-Learning │ →  │   Execute    │   │
│  │  (Planning)  │    │ (Strategy)   │    │   (Task)     │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│         ↑                                            ↓       │
│         │                                    ┌──────────────┐│
│         │                                    │ Auto-Review  ││
│         │                                    │  (Analysis)  ││
│         │                                    └──────────────┘│
│         │                                            ↓       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ Collective   │ ←  │   Skill      │ ←  │    Nudge     │   │
│  │Intelligence  │    │  Evolution   │    │  (Reminder)  │   │
│  │  (Sharing)   │    │(Optimization)│    │              │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## ⚙️ Configuration

Create a configuration file at `~/.openclaw/self_learning.yaml`:

```yaml
# Plan Mode
plan_mode:
  enabled: true
  auto_execute_threshold: medium
  show_risk_indicators: true

# Auto-Review
auto_review:
  enabled: true
  min_turn_count: 3
  save_to_memory: true

# Nudge System
nudge:
  enabled: true
  interval: 10
  counter_mode: mixed

# Skill Evolution
skill_evolution:
  enabled: true
  min_calls_for_analysis: 5
  auto_optimize: false

# Meta-Learning
meta_learning:
  enabled: true
  evolution_interval: 20
  exploration_rate: 0.2

# Collective Intelligence
collective_intelligence:
  enabled: true
  default_share_mode: vertical
  auto_share_threshold: 0.8
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific system tests
pytest tests/test_plan_mode.py
pytest tests/test_auto_review.py
pytest tests/test_skill_evolution.py
pytest tests/test_meta_learning.py
pytest tests/test_collective_intelligence.py

# Run with coverage
pytest --cov=openclaw_self_learning tests/
```

## 📊 Performance Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Plan Generation | < 100ms | ✅ |
| Strategy Selection | < 50ms | ✅ |
| Auto-Review | < 200ms | ✅ |
| Skill Tracking | < 10ms | ✅ |
| Knowledge Sharing | < 100ms | ✅ |

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Snowayai/openclaw-self-learning-skill.git
cd openclaw-self-learning-skill

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 openclaw_self_learning
black openclaw_self_learning
```

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Claude Code](https://github.com/anthropics/claude-code) Plan Mode
- Based on [Hermes Agent](https://github.com/NousResearch/hermes-agent) Nudge System
- Built for [OpenClaw](https://github.com/openclaw/openclaw) ecosystem

## 📮 Support

- 📧 Email: support@openclaw-self-learning.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 Issues: [GitHub Issues](https://github.com/Snowayai/openclaw-self-learning-skill/issues)

---

<div align="center">

**Made with ❤️ for the OpenClaw Community**

[⭐ Star us on GitHub](https://github.com/Snowayai/openclaw-self-learning-skill) •
[📖 Documentation](https://docs.openclaw-self-learning.dev) •
[🚀 Get Started](#quick-start)

</div>
