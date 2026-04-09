"""
Self-Learning Agent - Core integration of all six learning systems
"""
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime

from .config import SelfLearningConfig
from .systems.plan_mode import PlanModeSystem
from .systems.auto_review import AutoReviewSystem
from .systems.nudge import NudgeSystem
from .systems.skill_evolution import SkillEvolutionSystem
from .systems.meta_learning import MetaLearningSystem
from .systems.collective_intelligence import CollectiveIntelligenceSystem


class SelfLearningAgent:
    """
    A self-learning agent that integrates six learning systems
    
    Usage:
        agent = SelfLearningAgent(
            agent_id="my-agent",
            user_id="user-001",
            name="My Agent"
        )
        
        response = agent.process("Help me with this task")
    """
    
    def __init__(
        self,
        agent_id: str,
        user_id: str,
        name: str,
        config: Optional[SelfLearningConfig] = None,
        capabilities: Optional[List[str]] = None
    ):
        """
        Initialize the self-learning agent
        
        Args:
            agent_id: Unique agent identifier
            user_id: User identifier
            name: Agent name
            config: Configuration object (optional)
            capabilities: List of agent capabilities
        """
        self.agent_id = agent_id
        self.user_id = user_id
        self.name = name
        self.capabilities = capabilities or []
        self.config = config or SelfLearningConfig().load_or_create_default()
        
        # Initialize all learning systems
        self._init_systems()
        
        # Session tracking
        self.current_session: Optional[str] = None
        self.current_task: Optional[str] = None
    
    def _init_systems(self):
        """Initialize all learning systems"""
        # Plan Mode System
        self.plan_system = PlanModeSystem(
            config=self.config.plan_mode,
            data_dir=self.config.data_dir
        )
        
        # Auto-Review System
        self.review_system = AutoReviewSystem(
            config=self.config.auto_review,
            data_dir=self.config.data_dir
        )
        
        # Nudge System
        self.nudge_system = NudgeSystem(
            config=self.config.nudge,
            data_dir=self.config.data_dir
        )
        
        # Skill Evolution System
        self.evolution_system = SkillEvolutionSystem(
            config=self.config.skill_evolution,
            data_dir=self.config.data_dir
        )
        
        # Meta-Learning System
        self.meta_system = MetaLearningSystem(
            config=self.config.meta_learning,
            data_dir=self.config.data_dir
        )
        
        # Collective Intelligence System
        self.collective_system = CollectiveIntelligenceSystem(
            config=self.config.collective_intelligence,
            data_dir=self.config.data_dir,
            agent_id=self.agent_id,
            user_id=self.user_id,
            agent_name=self.name,
            capabilities=self.capabilities
        )
    
    def process(self, user_input: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input with all learning systems engaged
        
        This is the main entry point that orchestrates all six learning systems:
        1. Plan Mode - Generate and confirm execution plan
        2. Meta-Learning - Select optimal strategy
        3. Auto-Review - Track and analyze execution
        4. Nudge - Periodic reminders
        5. Skill Evolution - Track performance
        6. Collective Intelligence - Share and discover knowledge
        
        Args:
            user_input: User's input message
            session_id: Optional session identifier
            
        Returns:
            Response dictionary with results and metadata
        """
        # Generate or use provided session ID
        session_id = session_id or str(uuid.uuid4())
        self.current_session = session_id
        
        # Start tracking
        self._start_tracking(session_id, user_input)
        
        try:
            # Step 1: Plan Mode - Generate execution plan
            if self.config.plan_mode.enabled:
                plan_result = self._plan_execution(session_id, user_input)
                if plan_result.get('requires_confirmation'):
                    return plan_result
            
            # Step 2: Meta-Learning - Select strategy
            strategy = None
            if self.config.meta_learning.enabled:
                strategy = self.meta_system.select_strategy(user_input)
            
            # Step 3: Execute task
            execution_result = self._execute_task(
                session_id,
                user_input,
                strategy
            )
            
            # Step 4: Auto-Review - Analyze execution
            if self.config.auto_review.enabled:
                self._perform_review(session_id, user_input, execution_result)
            
            # Step 5: Check for Nudge
            nudge_message = None
            if self.config.nudge.enabled:
                nudge_message = self.nudge_system.check_nudge(session_id)
            
            # Step 6: Skill Evolution - Update tracking
            if self.config.skill_evolution.enabled:
                self.evolution_system.record_execution(
                    agent_id=self.agent_id,
                    success=execution_result.get('success', True),
                    execution_time=execution_result.get('duration_ms', 0)
                )
            
            # Step 7: Collective Intelligence - Share knowledge
            if self.config.collective_intelligence.enabled:
                self._share_knowledge_if_valuable(session_id, user_input, execution_result)
            
            # Build response
            response = {
                'content': execution_result.get('content', ''),
                'session_id': session_id,
                'success': execution_result.get('success', True),
            }
            
            if nudge_message:
                response['nudge'] = nudge_message
            
            if strategy:
                response['strategy_used'] = strategy.get('name')
            
            return response
            
        except Exception as e:
            # Handle errors
            self._handle_error(session_id, user_input, e)
            return {
                'content': f"Error processing request: {str(e)}",
                'session_id': session_id,
                'success': False,
                'error': str(e)
            }
        finally:
            # End tracking
            self._end_tracking(session_id)
    
    def _start_tracking(self, session_id: str, user_input: str):
        """Start tracking a new session"""
        self.current_task = user_input
        
        # Start Auto-Review tracking
        if self.config.auto_review.enabled:
            self.review_system.start_task(
                session_id=session_id,
                user_prompt=user_input
            )
        
        # Start Skill Evolution tracking
        if self.config.skill_evolution.enabled:
            self.evolution_system.track_usage_start(
                skill_name=self.name,
                session_id=session_id
            )
    
    def _plan_execution(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """Generate execution plan using Plan Mode"""
        plan = self.plan_system.create_plan(user_input, session_id)
        
        # Check if plan requires confirmation
        requires_confirmation = False
        if hasattr(plan, 'should_request_confirmation'):
            requires_confirmation = plan.should_request_confirmation()
        elif hasattr(plan, 'can_auto_execute'):
            requires_confirmation = not plan.can_auto_execute
        elif isinstance(plan, dict):
            requires_confirmation = plan.get('requires_confirmation', False)
        
        if requires_confirmation:
            return {
                'requires_confirmation': True,
                'plan': self.plan_system.display_plan(plan),
                'session_id': session_id,
                'message': 'Please review and confirm the execution plan'
            }
        
        return {'requires_confirmation': False}
    
    def _execute_task(
        self,
        session_id: str,
        user_input: str,
        strategy: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute the actual task"""
        import time
        start_time = time.time()
        
        # Record user input for Auto-Review
        if self.config.auto_review.enabled:
            self.review_system.record_message(
                session_id=session_id,
                role='user',
                content=user_input
            )
        
        # TODO: Implement actual task execution
        # This should be overridden or extended by subclasses
        content = f"Processed: {user_input}"
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            'content': content,
            'success': True,
            'duration_ms': execution_time
        }
    
    def _perform_review(
        self,
        session_id: str,
        user_input: str,
        execution_result: Dict[str, Any]
    ):
        """Perform auto-review after execution"""
        # Record assistant response
        self.review_system.record_message(
            session_id=session_id,
            role='assistant',
            content=execution_result.get('content', '')
        )
        
        # Complete task and trigger review
        review_result = self.review_system.complete_task(
            task_id=session_id,
            success=execution_result.get('success', True),
            error_message=execution_result.get('error')
        )
        
        # Save review results
        if review_result and review_result.get('has_lessons'):
            self.review_system.save_review(review_result)
    
    def _share_knowledge_if_valuable(
        self,
        session_id: str,
        user_input: str,
        execution_result: Dict[str, Any]
    ):
        """Share knowledge if it's valuable"""
        # Check if we should auto-share
        if execution_result.get('success') and execution_result.get('duration_ms', 0) > 1000:
            self.collective_system.share_knowledge(
                name=f"Task: {user_input[:50]}",
                description=f"Successfully completed: {user_input}",
                knowledge_type="workflow",
                content={
                    'input': user_input,
                    'result': execution_result,
                    'timestamp': datetime.now().isoformat()
                },
                source_system="self_learning_agent"
            )
    
    def _handle_error(self, session_id: str, user_input: str, error: Exception):
        """Handle execution errors"""
        # Record error for review
        if self.config.auto_review.enabled:
            self.review_system.complete_task(
                task_id=session_id,
                success=False,
                error_message=str(error)
            )
    
    def _end_tracking(self, session_id: str):
        """End tracking for the session"""
        # End Skill Evolution tracking
        if self.config.skill_evolution.enabled:
            self.evolution_system.track_usage_end(success=True)
        
        self.current_session = None
        self.current_task = None
    
    def confirm_plan(self, session_id: str, confirmed: bool = True) -> Dict[str, Any]:
        """
        Confirm or cancel a pending execution plan
        
        Args:
            session_id: Session identifier
            confirmed: Whether to confirm (True) or cancel (False)
            
        Returns:
            Response dictionary
        """
        if confirmed:
            return self.process("", session_id)
        else:
            return {
                'content': 'Plan cancelled by user',
                'session_id': session_id,
                'success': False,
                'cancelled': True
            }
    
    def get_learning_report(self) -> str:
        """Generate comprehensive learning report"""
        lines = [
            f"# Self-Learning Report for {self.name}",
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"\n## Agent Information",
            f"- ID: {self.agent_id}",
            f"- User: {self.user_id}",
            f"- Capabilities: {', '.join(self.capabilities)}",
        ]
        
        # Add reports from each system
        if self.config.skill_evolution.enabled:
            report = self.evolution_system.get_skill_report(self.name)
            if report:
                lines.extend(["\n## Skill Evolution", report])
        
        if self.config.collective_intelligence.enabled:
            report = self.collective_system.get_report()
            if report:
                lines.extend(["\n## Collective Intelligence", report.to_markdown()])
        
        return '\n'.join(lines)
    
    def discover_knowledge(self, context: Optional[str] = None) -> List[Dict[str, Any]]:
        """Discover relevant knowledge from collective intelligence"""
        if not self.config.collective_intelligence.enabled:
            return []
        
        return self.collective_system.get_recommendations(context)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'systems': {
                'plan_mode': self.config.plan_mode.enabled,
                'auto_review': self.config.auto_review.enabled,
                'nudge': self.config.nudge.enabled,
                'skill_evolution': self.config.skill_evolution.enabled,
                'meta_learning': self.config.meta_learning.enabled,
                'collective_intelligence': self.config.collective_intelligence.enabled,
            }
        }
