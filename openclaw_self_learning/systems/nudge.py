"""
Nudge System

Periodic reminders to save knowledge and create skills.
"""
from typing import Optional, Dict, Any
from datetime import datetime


class NudgeSystem:
    """Nudge System for periodic reminders"""
    
    def __init__(self, config=None, data_dir: Optional[str] = None):
        self.config = config
        self.data_dir = data_dir
        self._counters = {}
    
    def check_nudge(self, session_id: str) -> Optional[str]:
        """Check if nudge should be triggered"""
        if not self.config or not self.config.enabled:
            return None
        
        if session_id not in self._counters:
            self._counters[session_id] = 0
        
        self._counters[session_id] += 1
        
        # Check if threshold reached
        if self._counters[session_id] >= getattr(self.config, 'nudge_interval', 10):
            self._counters[session_id] = 0
            return self._generate_nudge_message()
        
        return None
    
    def _generate_nudge_message(self) -> str:
        """Generate nudge message"""
        messages = [
            "📝 Consider saving important insights to memory?",
            "💡 Worth creating a skill for this workflow?",
            "🧠 Should we document this lesson learned?",
            "🔄 This pattern might be reusable - save it?"
        ]
        
        import random
        return random.choice(messages)
    
    def increment_turn(self, session_id: str):
        """Increment turn counter"""
        if session_id not in self._counters:
            self._counters[session_id] = 0
        self._counters[session_id] += 1
    
    def reset_counter(self, session_id: str):
        """Reset counter for session"""
        self._counters[session_id] = 0
    
    def get_counter(self, session_id: str) -> int:
        """Get current counter value"""
        return self._counters.get(session_id, 0)
