"""
OpenClaw Skill Integration Example

This example shows how to integrate the Self-Learning Suite
into an existing OpenClaw Skill using the mixin class.
"""
from typing import Dict, Any
from openclaw_self_learning import SelfLearningSkillMixin


class SmartCodeAssistant(SelfLearningSkillMixin):
    """
    A smart code assistant that learns from every interaction
    
    This skill demonstrates how to integrate all six learning systems
    into an existing OpenClaw skill.
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize self-learning capabilities
        self.init_self_learning(
            agent_id="smart-code-assistant",
            user_id="user-001",
            agent_name="Smart Code Assistant",
            capabilities=["coding", "debugging", "code_review", "refactoring"]
        )
        
        # Configure systems
        self.configure_system('plan_mode', enabled=True)
        self.configure_system('auto_review', enabled=True)
        self.configure_system('meta_learning', enabled=True)
    
    def run(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """
        Main entry point for the skill
        
        This method orchestrates all six learning systems:
        1. Plan Mode - Generate execution plan
        2. Meta-Learning - Select optimal strategy
        3. Auto-Review - Track and analyze
        4. Nudge - Periodic reminders
        5. Skill Evolution - Performance tracking
        6. Collective Intelligence - Knowledge sharing
        """
        
        # Use the integrated learning system
        result = self.process_with_learning(
            session_id=session_id,
            user_input=user_input,
            process_func=lambda: self._execute_task(user_input)
        )
        
        # If plan requires confirmation, return immediately
        if result.get('requires_confirmation'):
            return {
                'type': 'plan',
                'content': result.get('plan'),
                'session_id': session_id,
                'requires_input': True
            }
        
        # Share valuable knowledge
        if result.get('success') and self._is_valuable_lesson(user_input):
            self.share_my_knowledge(
                name=f"Solution: {user_input[:50]}",
                description=f"Successfully solved: {user_input}",
                knowledge_type="skill",
                content={
                    'input': user_input,
                    'solution': result.get('content'),
                    'approach': result.get('strategy_used', 'default')
                },
                tags=["coding", "solution"]
            )
        
        return result
    
    def _execute_task(self, user_input: str) -> Dict[str, Any]:
        """Execute the actual task"""
        
        # Simulate task execution
        import time
        start_time = time.time()
        
        # Get selected strategy
        strategy = self.get_current_strategy()
        
        # Execute based on strategy
        if strategy and strategy.get('depth_level', 3) > 3:
            content = self._deep_analysis(user_input)
        else:
            content = self._quick_response(user_input)
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            'content': content,
            'success': True,
            'duration_ms': execution_time
        }
    
    def _deep_analysis(self, user_input: str) -> str:
        """Perform deep analysis"""
        return f"""
## Deep Analysis

**Input:** {user_input}

**Analysis:**
1. Identified the core issue
2. Analyzed multiple approaches
3. Recommended optimal solution

**Solution:**
Implement proper error handling and add logging for better debugging.

**Next Steps:**
1. Review the suggested changes
2. Test in your environment
3. Let me know if you need clarification
        """
    
    def _quick_response(self, user_input: str) -> str:
        """Provide quick response"""
        return f"Quick answer for: {user_input}\n\nTry adding try-except blocks around the problematic code."
    
    def _is_valuable_lesson(self, user_input: str) -> bool:
        """Determine if this is a valuable lesson to share"""
        # Simple heuristic: longer inputs with specific keywords
        valuable_keywords = ['debug', 'error', 'fix', 'optimize', 'refactor']
        return (
            len(user_input) > 20 and
            any(kw in user_input.lower() for kw in valuable_keywords)
        )
    
    def handle_confirmation(
        self,
        session_id: str,
        confirmed: bool
    ) -> Dict[str, Any]:
        """Handle plan confirmation"""
        if confirmed:
            return self.process_with_learning(session_id, "")
        else:
            return {
                'content': 'Plan cancelled. How else can I help?',
                'success': False,
                'cancelled': True
            }


# Usage example
def demo():
    """Demonstrate the smart code assistant"""
    print("🚀 Smart Code Assistant Demo\n")
    
    skill = SmartCodeAssistant()
    
    # Test 1: Simple question
    print("Test 1: Simple debugging question")
    print("-" * 50)
    result = skill.run("session-1", "How to fix IndexError?")
    print(f"Response: {result['content'][:100]}...")
    
    # Test 2: Complex task requiring planning
    print("\nTest 2: Complex refactoring task")
    print("-" * 50)
    result = skill.run("session-2", "Refactor this legacy codebase to use modern patterns")
    
    if result.get('type') == 'plan':
        print("Plan generated (user needs to confirm)")
        print(result['content'][:200])
    else:
        print(f"Response: {result['content'][:100]}...")
    
    # Test 3: Get learning report
    print("\nTest 3: Learning Report")
    print("-" * 50)
    report = skill.get_learning_report()
    print(report[:500])
    
    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo()
