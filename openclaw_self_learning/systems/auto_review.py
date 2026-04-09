"""
Auto-Review System

Post-execution analysis and lesson extraction.

This is a lightweight wrapper that imports from the full auto-review system.
For the complete implementation, see: /01-projects/auto-review-system/
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Try to import from full system
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "auto-review-system"))
    from auto_review_system import AutoReviewManager
    FULL_SYSTEM_AVAILABLE = True
except ImportError:
    FULL_SYSTEM_AVAILABLE = False


class AutoReviewSystem:
    """Auto-Review System for post-execution analysis"""
    
    def __init__(self, config=None, data_dir: Optional[str] = None):
        self.config = config
        self.data_dir = data_dir
        self._tasks = {}
        self._messages = {}
        
        if FULL_SYSTEM_AVAILABLE:
            try:
                # Try to create with config directly
                self._manager = AutoReviewManager(config)
            except Exception:
                # Fallback: create with proper wrapper config
                from auto_review_system.core import AutoReviewManagerConfig
                from auto_review_system.types import ReviewConfig
                review_config = ReviewConfig() if config is None else config
                wrapped_config = AutoReviewManagerConfig(
                    review_config=review_config,
                    workspace_path=data_dir
                )
                self._manager = AutoReviewManager(wrapped_config)
        else:
            self._manager = None
    
    def start_task(self, session_id: str, user_prompt: str) -> str:
        """Start tracking a task"""
        if self._manager:
            task = self._manager.start_task(session_id, user_prompt)
            return task.task_id
        
        self._tasks[session_id] = {
            'prompt': user_prompt,
            'start_time': datetime.now(),
            'messages': []
        }
        self._messages[session_id] = []
        return session_id
    
    def record_message(
        self,
        session_id: str,
        role: str,
        content: str,
        tool_calls: Optional[List] = None
    ):
        """Record a conversation message"""
        if self._manager:
            self._manager.record_message(session_id, role, content, tool_calls)
            return
        
        if session_id not in self._messages:
            self._messages[session_id] = []
        
        self._messages[session_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })
    
    def record_tool_usage(self, task_id: str, tool_name: str):
        """Record tool usage"""
        if self._manager:
            self._manager.record_tool_usage(task_id, tool_name)
    
    def complete_task(
        self,
        task_id: str,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Complete task and trigger review"""
        if self._manager:
            result = self._manager.complete_task(task_id, success, error_message)
            if result:
                return {
                    'has_lessons': result.has_valuable_lessons,
                    'lesson_count': len(result.lessons),
                    'summary': result.summary,
                    'key_takeaway': result.key_takeaway
                }
            return None
        
        # Fallback implementation
        task = self._tasks.get(task_id, {})
        messages = self._messages.get(task_id, [])
        
        review = {
            'task_id': task_id,
            'success': success,
            'has_lessons': len(messages) > 3,
            'lesson_count': len(messages) // 3,
            'summary': f"Task completed with {len(messages)} messages",
            'key_takeaway': 'Review conversation patterns' if not success else 'Good execution',
            'insights': []
        }
        
        if not success:
            review['insights'].append(f'Error: {error_message}')
        
        return review
    
    def save_review(self, review_result: Dict[str, Any]) -> bool:
        """Save review to memory"""
        if self._manager:
            return bool(self._manager.save_review(review_result))
        
        # Minimal implementation: just print
        print(f"📋 Auto-Review: {review_result.get('summary', '')}")
        if review_result.get('key_takeaway'):
            print(f"💡 Key takeaway: {review_result['key_takeaway']}")
        return True
