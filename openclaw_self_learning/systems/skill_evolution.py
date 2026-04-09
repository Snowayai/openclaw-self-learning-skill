"""
Skill Evolution System

Performance tracking and automatic optimization.
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Try to import from full system
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "skill-evolution-system"))
    from skill_evolution_system import SkillEvolutionManager
    FULL_SYSTEM_AVAILABLE = True
except ImportError:
    FULL_SYSTEM_AVAILABLE = False


class SkillEvolutionSystem:
    """Skill Evolution System for performance tracking"""
    
    def __init__(self, config=None, data_dir: Optional[str] = None):
        self.config = config
        self.data_dir = data_dir
        self._usage_data = {}
        self._start_times = {}
        
        if FULL_SYSTEM_AVAILABLE:
            try:
                from skill_evolution_system.core import EvolutionManagerConfig
                from skill_evolution_system.types import EvolutionConfig
                evolution_config = EvolutionConfig() if config is None else config
                wrapped_config = EvolutionManagerConfig(
                    evolution_config=evolution_config,
                    data_dir=data_dir
                )
                self._manager = SkillEvolutionManager(wrapped_config)
            except Exception:
                self._manager = None
        else:
            self._manager = None
    
    def track_usage_start(self, skill_name: str, session_id: str):
        """Start tracking usage"""
        if self._manager:
            self._manager.track_usage_start(skill_name, session_id)
            return
        
        self._start_times[session_id] = datetime.now()
        if skill_name not in self._usage_data:
            self._usage_data[skill_name] = {
                'total_calls': 0,
                'success_count': 0,
                'failure_count': 0,
                'total_duration_ms': 0
            }
    
    def track_usage_end(self, success: bool = True, error_message: Optional[str] = None) -> Optional[Dict]:
        """End tracking usage"""
        if self._manager:
            return self._manager.track_usage_end(success, error_message)
        
        # Fallback: calculate duration
        return {'success': success}
    
    def record_execution(
        self,
        agent_id: str,
        success: bool,
        execution_time: int
    ):
        """Record execution"""
        if self._manager:
            # Note: This would need proper integration
            pass
        
        # Fallback tracking
        if agent_id not in self._usage_data:
            self._usage_data[agent_id] = {
                'total_calls': 0,
                'success_count': 0,
                'failure_count': 0,
                'total_duration_ms': 0
            }
        
        data = self._usage_data[agent_id]
        data['total_calls'] += 1
        data['total_duration_ms'] += execution_time
        
        if success:
            data['success_count'] += 1
        else:
            data['failure_count'] += 1
    
    def record_tool(self, skill_name: str, tool_name: str):
        """Record tool usage"""
        # Tracking for future analysis
        pass
    
    def get_skill_report(self, skill_name: str) -> Optional[str]:
        """Get skill evolution report"""
        if self._manager:
            report = self._manager.get_skill_report(skill_name)
            return report if report else "No data available"
        
        data = self._usage_data.get(skill_name, {})
        if not data or data['total_calls'] == 0:
            return "No usage data available"
        
        success_rate = data['success_count'] / data['total_calls']
        avg_duration = data['total_duration_ms'] / data['total_calls']
        
        return f"""
## Skill Evolution Report: {skill_name}

**Usage Statistics:**
- Total calls: {data['total_calls']}
- Success rate: {success_rate:.1%}
- Average duration: {avg_duration:.0f}ms
- Failures: {data['failure_count']}

**Recommendation:** Continue monitoring performance
        """
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get dashboard data"""
        if self._manager:
            return self._manager.get_dashboard_data()
        
        return {
            'total_skills': len(self._usage_data),
            'skills': [
                {
                    'name': name,
                    'calls': data['total_calls'],
                    'success_rate': data['success_count'] / data['total_calls'] if data['total_calls'] > 0 else 0
                }
                for name, data in self._usage_data.items()
            ]
        }


# Minimal config class for compatibility
class EvolutionManagerConfig:
    def __init__(self, evolution_config=None, data_dir=None):
        self.evolution_config = evolution_config
        self.data_dir = data_dir
