"""
Meta-Learning System

Strategy selection and evolution using genetic algorithms.
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Try to import from full system
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "meta-learning-system"))
    from meta_learning_system import MetaLearningManager
    FULL_SYSTEM_AVAILABLE = True
except ImportError:
    FULL_SYSTEM_AVAILABLE = False


class MetaLearningSystem:
    """Meta-Learning System for strategy optimization"""
    
    def __init__(self, config=None, data_dir: Optional[str] = None):
        self.config = config
        self.data_dir = data_dir
        
        # Default strategies
        self._strategies = [
            {
                'id': 'deep_analysis',
                'name': 'Deep Analysis',
                'type': 'deep_analysis',
                'depth_level': 5,
                'speed_priority': 0.2,
                'suitable_for': ['analysis', 'debugging', 'research']
            },
            {
                'id': 'quick_answer',
                'name': 'Quick Answer',
                'type': 'quick_answer',
                'depth_level': 2,
                'speed_priority': 0.9,
                'suitable_for': ['qna', 'general']
            },
            {
                'id': 'step_by_step',
                'name': 'Step by Step',
                'type': 'step_by_step',
                'depth_level': 4,
                'speed_priority': 0.4,
                'suitable_for': ['debugging', 'planning', 'teaching']
            },
            {
                'id': 'creative',
                'name': 'Creative',
                'type': 'creative',
                'depth_level': 3,
                'speed_priority': 0.5,
                'suitable_for': ['creation', 'innovation']
            }
        ]
        
        self._executions = []
        
        if FULL_SYSTEM_AVAILABLE:
            try:
                from meta_learning_system.core import MetaLearningManagerConfig
                wrapped_config = MetaLearningManagerConfig(
                    meta_config=config,
                    data_dir=data_dir
                )
                self._manager = MetaLearningManager(wrapped_config)
            except Exception:
                self._manager = None
        else:
            self._manager = None
    
    def select_strategy(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Select best strategy for the task"""
        if self._manager:
            strategy = self._manager.select_strategy(user_input)
            if strategy:
                return {
                    'id': strategy.id,
                    'name': strategy.name,
                    'type': strategy.type.value,
                    'depth_level': strategy.depth_level,
                    'speed_priority': strategy.speed_priority
                }
        
        # Fallback: simple keyword matching
        input_lower = user_input.lower()
        
        if any(kw in input_lower for kw in ['debug', 'fix', 'error', 'bug']):
            return self._strategies[0]  # Deep analysis
        elif any(kw in input_lower for kw in ['create', 'build', 'design']):
            return self._strategies[3]  # Creative
        elif any(kw in input_lower for kw in ['how', 'what', 'why']):
            return self._strategies[1]  # Quick answer
        else:
            return self._strategies[2]  # Step by step
    
    def record_execution(
        self,
        strategy_id: str,
        task_category: str,
        success: bool,
        execution_time_ms: int,
        user_satisfaction: Optional[float] = None
    ):
        """Record strategy execution"""
        if self._manager:
            # Would need proper category enum
            pass
        
        self._executions.append({
            'strategy_id': strategy_id,
            'success': success,
            'execution_time': execution_time_ms,
            'satisfaction': user_satisfaction
        })
    
    def get_strategy_report(self) -> Any:
        """Get strategy performance report"""
        if self._manager:
            return self._manager.get_strategy_report()
        
        # Fallback: simple statistics
        if not self._executions:
            return type('Report', (), {
                'to_markdown': lambda: "# Strategy Report\n\nNo execution data available."
            })()
        
        success_rate = sum(1 for e in self._executions if e['success']) / len(self._executions)
        avg_time = sum(e['execution_time'] for e in self._executions) / len(self._executions)
        
        return type('Report', (), {
            'to_markdown': lambda: f"""
# Meta-Learning Strategy Report

**Performance Summary:**
- Total executions: {len(self._executions)}
- Success rate: {success_rate:.1%}
- Average execution time: {avg_time:.0f}ms

**Active Strategies:**
{chr(10).join([f"- {s['name']} (depth: {s['depth_level']})" for s in self._strategies])}

**Recommendation:** Continue monitoring strategy effectiveness
            """
        })()


# Minimal config class
class MetaLearningManagerConfig:
    def __init__(self, meta_config=None, data_dir=None):
        self.meta_config = meta_config
        self.data_dir = data_dir
