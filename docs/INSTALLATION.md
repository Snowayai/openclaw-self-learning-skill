# Installation Guide

This guide will help you install and set up the OpenClaw Self-Learning Suite.

## Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- Git (for development installation)

## Quick Installation

### From PyPI (Recommended)

```bash
pip install openclaw-self-learning-suite
```

### From Source

```bash
git clone https://github.com/openclaw/openclaw-self-learning-suite.git
cd openclaw-self-learning-suite
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/openclaw/openclaw-self-learning-suite.git
cd openclaw-self-learning-suite
pip install -e ".[dev]"
```

## Verification

Test your installation:

```python
from openclaw_self_learning import SelfLearningAgent

agent = SelfLearningAgent(
    agent_id="test",
    user_id="test",
    name="Test Agent"
)

print(f"✅ Installation successful! Agent: {agent.name}")
```

## Configuration

### Create Configuration File

```bash
# Create default configuration
python -c "from openclaw_self_learning import SelfLearningConfig; SelfLearningConfig().load_or_create_default()"
```

This creates `~/.openclaw/self_learning.yaml`:

```yaml
debug: false
data_dir: null
plan_mode:
  enabled: true
  auto_execute_threshold: medium
  show_risk_indicators: true
  show_estimated_time: true
  allow_modification: true
auto_review:
  enabled: true
  auto_review_on_complete: true
  auto_review_on_fail: true
  min_turn_count: 3
  min_duration_seconds: 30
  save_to_daily_memory: true
  save_to_long_term_memory: true
  save_threshold: 0.7
nudge:
  enabled: true
  nudge_interval: 10
  counter_mode: mixed
  min_tool_calls: 3
  cooldown_seconds: 120
  reset_on_skill_save: true
  reset_on_memory_save: true
skill_evolution:
  enabled: true
  min_calls_for_analysis: 5
  analysis_interval_calls: 10
  success_rate_threshold: 0.8
  duration_threshold_ms: 5000
  generate_optimizations: true
  auto_apply_optimizations: false
  max_optimizations_per_skill: 3
  enable_versioning: true
meta_learning:
  enabled: true
  initial_strategy_count: 10
  max_strategy_count: 50
  enable_evolution: true
  evolution_interval: 20
  mutation_rate: 0.1
  crossover_rate: 0.3
  exploration_rate: 0.2
collective_intelligence:
  enabled: true
  enable_sharing: true
  enable_importing: true
  auto_share_threshold: 0.8
  auto_sync: true
  sync_interval_minutes: 60
  enable_discovery: true
  recommendation_count: 5
  default_share_mode: vertical
```

### Customize Configuration

Edit `~/.openclaw/self_learning.yaml`:

```yaml
# Example: Disable plan mode for simple tasks
plan_mode:
  enabled: false

# Example: More frequent nudges
nudge:
  nudge_interval: 5

# Example: Stricter auto-review
auto_review:
  min_turn_count: 5
```

## Integration with OpenClaw

### As a Skill

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
        return self.process_with_learning(session_id, user_input)
```

### As a Standalone Agent

```python
from openclaw_self_learning import SelfLearningAgent

agent = SelfLearningAgent(
    agent_id="my-agent",
    user_id="user-001",
    name="My Learning Agent"
)

response = agent.process("Help me with this task")
print(response['content'])
```

## Troubleshooting

### Import Error

If you get `ModuleNotFoundError`:

```bash
# Reinstall
pip uninstall openclaw-self-learning-suite
pip install openclaw-self-learning-suite

# Or install from source
pip install -e .
```

### Configuration Not Loading

```bash
# Remove old config
rm ~/.openclaw/self_learning.yaml

# Recreate
python -c "from openclaw_self_learning import SelfLearningConfig; SelfLearningConfig().load_or_create_default()"
```

### Permission Issues

```bash
# Install with user permissions
pip install --user openclaw-self-learning-suite

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install openclaw-self-learning-suite
```

## Next Steps

- Read the [Architecture Overview](ARCHITECTURE.md)
- Check out [Examples](../examples/)
- Review [API Reference](API.md)

## Getting Help

- 📖 [Documentation](https://docs.openclaw-self-learning.dev)
- 💬 [Discord](https://discord.gg/openclaw)
- 🐛 [GitHub Issues](https://github.com/openclaw/openclaw-self-learning-suite/issues)
