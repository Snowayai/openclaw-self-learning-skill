"""
Self-Learning Skill Mixin for OpenClaw Integration

This mixin allows any OpenClaw skill to easily integrate all six learning systems.

Usage:
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
"""
from typing import Optional, Dict, Any, List

from .config import SelfLearningConfig
from .agent import SelfLearningAgent


class SelfLearningSkillMixin:
    """
    Mixin class for integrating self-learning capabilities into OpenClaw skills
    
    This mixin provides seamless integration of all six learning systems:
    - Plan Mode for pre-execution planning
    - Auto-Review for post-execution analysis
    - Nudge System for periodic reminders
    - Skill Evolution for performance tracking
    - Meta-Learning for strategy optimization
    - Collective Intelligence for knowledge sharing
    """
    
    def __init__(self):
        super().__init__()
        self.self_learning_agent: Optional[SelfLearningAgent] = None
        self._self_learning_enabled = True
        self._config: Optional[SelfLearningConfig] = None
    
    def init_self_learning(
        self,
        agent_id: str,
        user_id: str,
        agent_name: str,
        config: Optional[SelfLearningConfig] = None,
        capabilities: Optional[List[str]] = None,
        data_dir: Optional[str] = None
    ):
        """
        Initialize self-learning capabilities
        
        Args:
            agent_id: Unique identifier for this skill/agent
            user_id: User identifier
            agent_name: Human-readable name
            config: SelfLearningConfig instance (optional)
            capabilities: List of skill capabilities
            data_dir: Directory for storing learning data
        """
        # Load or create configuration
        if config is None:
            self._config = SelfLearningConfig()
            if data_dir:
                self._config.data_dir = data_dir
            self._config = self._config.load_or_create_default()
        else:
            self._config = config
        
        # Create self-learning agent
        self.self_learning_agent = SelfLearningAgent(
            agent_id=agent_id,
            user_id=user_id,
            name=agent_name,
            config=self._config,
            capabilities=capabilities
        )
        
        return self
    
    def enable_self_learning(self):
        """Enable self-learning systems"""
        self._self_learning_enabled = True
        return self
    
    def disable_self_learning(self):
        """Disable self-learning systems"""
        self._self_learning_enabled = False
        return self
    
    def process_with_learning(
        self,
        session_id: str,
        user_input: str,
        process_func: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Process user input with all learning systems engaged
        
        This is the main method that orchestrates all six learning systems
        around the skill's core functionality.
        
        Args:
            session_id: Session identifier
            user_input: User's input
            process_func: Optional custom processing function
            
        Returns:
            Response dictionary with learning metadata
        """
        if not self._self_learning_enabled or not self.self_learning_agent:
            # Fallback to basic processing
            if process_func:
                return process_func()
            return {'content': 'Self-learning not initialized'}
        
        # Use the self-learning agent to process
        try:
            response = self.self_learning_agent.process(user_input, session_id)
            
            # If plan confirmation is required, return immediately
            if response.get('requires_confirmation'):
                return response
            
            # Execute the actual skill logic if provided
            if process_func and not response.get('content'):
                execution_result = process_func()
                response['content'] = execution_result.get('content', '')
            
            return response
            
        except Exception as e:
            return {
                'content': f'Error in self-learning processing: {str(e)}',
                'session_id': session_id,
                'success': False,
                'error': str(e)
            }
    
    def start_learning_session(self, session_id: str, user_input: str):
        """
        Explicitly start a learning session
        
        Call this at the beginning of your skill's run() method
        """
        if self.self_learning_agent:
            self.self_learning_agent._start_tracking(session_id, user_input)
    
    def end_learning_session(
        self,
        session_id: str,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """
        Explicitly end a learning session
        
        Call this at the end of your skill's run() method
        """
        if self.self_learning_agent:
            # Perform review
            if self._config.auto_review.enabled:
                self.self_learning_agent._perform_review(
                    session_id,
                    self.self_learning_agent.current_task or '',
                    {'success': success, 'error': error_message}
                )
            
            # End tracking
            self.self_learning_agent._end_tracking(session_id)
    
    def record_user_message(self, session_id: str, content: str):
        """Record a user message for learning"""
        if self.self_learning_agent and self._config.auto_review.enabled:
            self.self_learning_agent.review_system.record_message(
                session_id=session_id,
                role='user',
                content=content
            )
    
    def record_assistant_message(
        self,
        session_id: str,
        content: str,
        tool_calls: Optional[List] = None
    ):
        """Record an assistant message for learning"""
        if self.self_learning_agent and self._config.auto_review.enabled:
            self.self_learning_agent.review_system.record_message(
                session_id=session_id,
                role='assistant',
                content=content,
                tool_calls=tool_calls
            )
    
    def record_tool_usage(self, tool_name: str):
        """Record tool usage for tracking"""
        if self.self_learning_agent:
            # Track in review system
            if self._config.auto_review.enabled:
                self.self_learning_agent.review_system.record_tool_usage(
                    task_id=self.self_learning_agent.current_session,
                    tool_name=tool_name
                )
            
            # Track in evolution system
            if self._config.skill_evolution.enabled:
                self.self_learning_agent.evolution_system.record_tool(
                    skill_name=self.self_learning_agent.name,
                    tool_name=tool_name
                )
    
    def share_my_knowledge(
        self,
        name: str,
        description: str,
        knowledge_type: str,
        content: Dict[str, Any],
        tags: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Share knowledge to collective intelligence
        
        Returns:
            Package ID if successful
        """
        if not self.self_learning_agent or not self._config.collective_intelligence.enabled:
            return None
        
        from .systems.collective_intelligence.types import KnowledgeType
        
        kt = KnowledgeType(knowledge_type) if knowledge_type else KnowledgeType.SKILL
        
        return self.self_learning_agent.collective_system.share_knowledge(
            name=name,
            description=description,
            knowledge_type=kt,
            content=content,
            source_system="openclaw_skill",
            tags=tags or []
        )
    
    def discover_knowledge(self, context: Optional[str] = None) -> List[Dict[str, Any]]:
        """Discover relevant knowledge from collective intelligence"""
        if not self.self_learning_agent or not self._config.collective_intelligence.enabled:
            return []
        
        return self.self_learning_agent.discover_knowledge(context)
    
    def import_discovered_knowledge(self, package_id: str) -> bool:
        """Import a discovered knowledge package"""
        if not self.self_learning_agent or not self._config.collective_intelligence.enabled:
            return False
        
        return self.self_learning_agent.collective_system.import_knowledge(package_id)
    
    def get_learning_report(self) -> str:
        """Get comprehensive learning report"""
        if not self.self_learning_agent:
            return "Self-learning not initialized"
        
        return self.self_learning_agent.get_learning_report()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        if not self.self_learning_agent:
            return {'error': 'Not initialized'}
        
        return self.self_learning_agent.get_stats()
    
    def configure_system(self, system_name: str, **kwargs):
        """
        Configure a specific learning system
        
        Args:
            system_name: Name of the system (plan_mode, auto_review, etc.)
            **kwargs: Configuration parameters
        """
        if not self._config:
            return
        
        if system_name == 'plan_mode':
            for key, value in kwargs.items():
                setattr(self._config.plan_mode, key, value)
        elif system_name == 'auto_review':
            for key, value in kwargs.items():
                setattr(self._config.auto_review, key, value)
        elif system_name == 'nudge':
            for key, value in kwargs.items():
                setattr(self._config.nudge, key, value)
        elif system_name == 'skill_evolution':
            for key, value in kwargs.items():
                setattr(self._config.skill_evolution, key, value)
        elif system_name == 'meta_learning':
            for key, value in kwargs.items():
                setattr(self._config.meta_learning, key, value)
        elif system_name == 'collective_intelligence':
            for key, value in kwargs.items():
                setattr(self._config.collective_intelligence, key, value)
        
        # Save updated configuration
        self._config.to_file(self._config.get_default_config_path())
