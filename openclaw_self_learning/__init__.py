"""
OpenClaw Self-Learning Suite

A comprehensive self-learning ecosystem for OpenClaw agents.
Integrates six learning systems for continuous improvement.
"""

__version__ = "1.0.0"
__author__ = "OpenClaw Community"
__license__ = "MIT"

# Core imports
from .agent import SelfLearningAgent
from .skill_mixin import SelfLearningSkillMixin
from .config import SelfLearningConfig

# System imports
from .systems.plan_mode import PlanModeSystem
from .systems.auto_review import AutoReviewSystem
from .systems.nudge import NudgeSystem
from .systems.skill_evolution import SkillEvolutionSystem
from .systems.meta_learning import MetaLearningSystem
from .systems.collective_intelligence import CollectiveIntelligenceSystem

__all__ = [
    # Core
    'SelfLearningAgent',
    'SelfLearningSkillMixin',
    'SelfLearningConfig',
    # Systems
    'PlanModeSystem',
    'AutoReviewSystem',
    'NudgeSystem',
    'SkillEvolutionSystem',
    'MetaLearningSystem',
    'CollectiveIntelligenceSystem',
]
