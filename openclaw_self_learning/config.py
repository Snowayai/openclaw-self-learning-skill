"""
Configuration management for Self-Learning Suite
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import yaml
from pathlib import Path


@dataclass
class PlanModeConfig:
    """Plan Mode configuration"""
    enabled: bool = True
    auto_execute_threshold: str = "medium"  # low, medium, high
    show_risk_indicators: bool = True
    show_estimated_time: bool = True
    show_step_details: bool = True
    allow_modification: bool = True


@dataclass
class AutoReviewConfig:
    """Auto-Review configuration"""
    enabled: bool = True
    auto_review_on_complete: bool = True
    auto_review_on_fail: bool = True
    min_turn_count: int = 3
    min_duration_seconds: int = 30
    save_to_daily_memory: bool = True
    save_to_long_term_memory: bool = True
    save_threshold: float = 0.7


@dataclass
class NudgeConfig:
    """Nudge System configuration"""
    enabled: bool = True
    nudge_interval: int = 10
    counter_mode: str = "mixed"  # turn, tool, mixed
    min_tool_calls: int = 3
    cooldown_seconds: int = 120
    reset_on_skill_save: bool = True
    reset_on_memory_save: bool = True


@dataclass
class SkillEvolutionConfig:
    """Skill Evolution configuration"""
    enabled: bool = True
    min_calls_for_analysis: int = 5
    analysis_interval_calls: int = 10
    success_rate_threshold: float = 0.8
    duration_threshold_ms: int = 5000
    generate_optimizations: bool = True
    auto_apply_optimizations: bool = False
    max_optimizations_per_skill: int = 3
    enable_versioning: bool = True


@dataclass
class MetaLearningConfig:
    """Meta-Learning configuration"""
    enabled: bool = True
    initial_strategy_count: int = 10
    max_strategy_count: int = 50
    enable_evolution: bool = True
    evolution_interval: int = 20
    mutation_rate: float = 0.1
    crossover_rate: float = 0.3
    exploration_rate: float = 0.2


@dataclass
class CollectiveIntelligenceConfig:
    """Collective Intelligence configuration"""
    enabled: bool = True
    enable_sharing: bool = True
    enable_importing: bool = True
    auto_share_threshold: float = 0.8
    auto_sync: bool = True
    sync_interval_minutes: int = 60
    enable_discovery: bool = True
    recommendation_count: int = 5
    default_share_mode: str = "vertical"


@dataclass
class SelfLearningConfig:
    """Main configuration class"""
    # Global settings
    debug: bool = False
    data_dir: Optional[str] = None
    
    # System configurations
    plan_mode: PlanModeConfig = field(default_factory=PlanModeConfig)
    auto_review: AutoReviewConfig = field(default_factory=AutoReviewConfig)
    nudge: NudgeConfig = field(default_factory=NudgeConfig)
    skill_evolution: SkillEvolutionConfig = field(default_factory=SkillEvolutionConfig)
    meta_learning: MetaLearningConfig = field(default_factory=MetaLearningConfig)
    collective_intelligence: CollectiveIntelligenceConfig = field(
        default_factory=CollectiveIntelligenceConfig
    )
    
    @classmethod
    def from_file(cls, config_path: str) -> "SelfLearningConfig":
        """Load configuration from YAML file"""
        path = Path(config_path)
        if not path.exists():
            return cls()
        
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data or {})
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SelfLearningConfig":
        """Create configuration from dictionary"""
        config = cls()
        
        if 'plan_mode' in data:
            config.plan_mode = PlanModeConfig(**data['plan_mode'])
        if 'auto_review' in data:
            config.auto_review = AutoReviewConfig(**data['auto_review'])
        if 'nudge' in data:
            config.nudge = NudgeConfig(**data['nudge'])
        if 'skill_evolution' in data:
            config.skill_evolution = SkillEvolutionConfig(**data['skill_evolution'])
        if 'meta_learning' in data:
            config.meta_learning = MetaLearningConfig(**data['meta_learning'])
        if 'collective_intelligence' in data:
            config.collective_intelligence = CollectiveIntelligenceConfig(
                **data['collective_intelligence']
            )
        
        return config
    
    def to_file(self, config_path: str):
        """Save configuration to YAML file"""
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'debug': self.debug,
            'data_dir': self.data_dir,
            'plan_mode': self.plan_mode.__dict__,
            'auto_review': self.auto_review.__dict__,
            'nudge': self.nudge.__dict__,
            'skill_evolution': self.skill_evolution.__dict__,
            'meta_learning': self.meta_learning.__dict__,
            'collective_intelligence': self.collective_intelligence.__dict__,
        }
    
    def get_default_config_path(self) -> str:
        """Get default configuration file path"""
        return str(Path.home() / ".openclaw" / "self_learning.yaml")
    
    def load_or_create_default(self) -> "SelfLearningConfig":
        """Load default configuration or create if not exists"""
        config_path = self.get_default_config_path()
        
        if Path(config_path).exists():
            return SelfLearningConfig.from_file(config_path)
        
        # Create default configuration
        config = SelfLearningConfig()
        config.to_file(config_path)
        return config
