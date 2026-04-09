"""
Plan Mode System

Pre-execution planning with user confirmation and risk assessment.

This is a lightweight wrapper that imports from the full plan-mode system.
For the complete implementation, see: /01-projects/plan-mode/
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Try to import from full system, fallback to minimal implementation
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "plan-mode"))
    from plan_system import PlanManager, PlanManagerConfig
    from plan_system.types import Plan
    FULL_SYSTEM_AVAILABLE = True
except ImportError:
    FULL_SYSTEM_AVAILABLE = False


class PlanModeSystem:
    """Plan Mode System for pre-execution planning"""
    
    def __init__(self, config=None, data_dir: Optional[str] = None):
        self.config = config
        self.data_dir = data_dir
        
        if FULL_SYSTEM_AVAILABLE:
            self._manager = PlanManager(config)
        else:
            self._manager = None
            self._plans = {}
    
    def create_plan(self, user_input: str, session_id: str) -> Any:
        """Create an execution plan"""
        if self._manager:
            return self._manager.create_plan(user_input, session_id)
        
        # Minimal fallback implementation
        plan = {
            'id': session_id,
            'steps': [
                {'description': f'Analyze: {user_input[:50]}...', 'risk': 'low'},
                {'description': 'Execute task', 'risk': 'medium'},
                {'description': 'Verify results', 'risk': 'low'}
            ],
            'requires_confirmation': True
        }
        self._plans[session_id] = plan
        return type('Plan', (), {
            'should_request_confirmation': lambda: True,
            'steps': plan['steps'],
            '__repr__': lambda: f"Plan({len(plan['steps'])} steps)"
        })()
    
    def display_plan(self, plan) -> str:
        """Display plan in human-readable format"""
        if self._manager:
            return self._manager.display_plan(plan)
        
        lines = ["📋 Execution Plan", "=" * 50]
        for i, step in enumerate(getattr(plan, 'steps', []), 1):
            risk = step.get('risk', 'low') if isinstance(step, dict) else 'low'
            desc = step.get('description', str(step)) if isinstance(step, dict) else str(step)
            lines.append(f"{i}. [{risk.upper()}] {desc}")
        lines.extend(["", "Confirm to proceed? (yes/no/modify)"])
        return '\n'.join(lines)
    
    def handle_confirmation(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """Handle user confirmation"""
        if self._manager:
            return self._manager.handle_user_response(session_id, user_input)
        
        input_lower = user_input.lower().strip()
        if input_lower in ['yes', 'y', 'confirm', '确认']:
            return {'success': True, 'action': 'execute'}
        elif input_lower in ['no', 'n', 'cancel', '取消']:
            return {'success': False, 'action': 'cancel'}
        else:
            return {'success': False, 'action': 'unknown', 'message': 'Please confirm: yes/no'}
