"""
Basic tests for OpenClaw Self-Learning Suite
"""
import pytest
from openclaw_self_learning import (
    SelfLearningAgent,
    SelfLearningConfig,
    PlanModeSystem,
    AutoReviewSystem,
    NudgeSystem,
    SkillEvolutionSystem,
    MetaLearningSystem,
    CollectiveIntelligenceSystem,
)


class TestSelfLearningAgent:
    """Tests for SelfLearningAgent"""
    
    def test_agent_creation(self):
        """Test agent initialization"""
        agent = SelfLearningAgent(
            agent_id="test-agent",
            user_id="test-user",
            name="Test Agent"
        )
        
        assert agent.agent_id == "test-agent"
        assert agent.user_id == "test-user"
        assert agent.name == "Test Agent"
    
    def test_agent_processing(self):
        """Test basic processing"""
        agent = SelfLearningAgent(
            agent_id="test-agent",
            user_id="test-user",
            name="Test Agent"
        )
        
        # Disable plan mode for this test to avoid confirmation
        agent.config.plan_mode.enabled = False
        
        response = agent.process("Test input")
        
        assert response is not None
        assert 'content' in response
        assert 'session_id' in response


class TestPlanModeSystem:
    """Tests for PlanModeSystem"""
    
    def test_plan_creation(self):
        """Test plan creation"""
        system = PlanModeSystem()
        plan = system.create_plan("Test task", "session-1")
        
        assert plan is not None
    
    def test_plan_display(self):
        """Test plan display"""
        system = PlanModeSystem()
        plan = system.create_plan("Test task", "session-1")
        display = system.display_plan(plan)
        
        assert isinstance(display, str)
        assert len(display) > 0


class TestAutoReviewSystem:
    """Tests for AutoReviewSystem"""
    
    def test_task_tracking(self):
        """Test task tracking"""
        system = AutoReviewSystem()
        task_id = system.start_task("session-1", "Test task")
        
        # Task ID should be returned (might be session-1 or generated)
        assert task_id is not None
        assert len(task_id) > 0
    
    def test_message_recording(self):
        """Test message recording"""
        system = AutoReviewSystem()
        system.start_task("session-1", "Test task")
        
        system.record_message("session-1", "user", "Hello")
        system.record_message("session-1", "assistant", "Hi")
        
        # Should not raise
        assert True


class TestNudgeSystem:
    """Tests for NudgeSystem"""
    
    def test_nudge_check(self):
        """Test nudge checking"""
        from openclaw_self_learning.config import NudgeConfig
        
        config = NudgeConfig(nudge_interval=2, enabled=True)
        system = NudgeSystem(config=config)
        
        # First check - no nudge
        result = system.check_nudge("session-1")
        assert result is None
        
        # Second check - still no nudge
        result = system.check_nudge("session-1")
        assert result is not None  # Should trigger nudge


class TestSkillEvolutionSystem:
    """Tests for SkillEvolutionSystem"""
    
    def test_usage_tracking(self):
        """Test usage tracking"""
        system = SkillEvolutionSystem()
        system.track_usage_start("test-skill", "session-1")
        
        result = system.track_usage_end(success=True)
        assert result is not None


class TestMetaLearningSystem:
    """Tests for MetaLearningSystem"""
    
    def test_strategy_selection(self):
        """Test strategy selection"""
        system = MetaLearningSystem()
        strategy = system.select_strategy("Debug this error")
        
        assert strategy is not None
        assert 'name' in strategy
        assert 'type' in strategy


class TestCollectiveIntelligenceSystem:
    """Tests for CollectiveIntelligenceSystem"""
    
    def test_knowledge_sharing(self):
        """Test knowledge sharing"""
        from openclaw_self_learning.systems.collective_intelligence import KnowledgeType
        
        system = CollectiveIntelligenceSystem(
            agent_id="test-agent",
            user_id="test-user",
            agent_name="Test Agent"
        )
        
        package_id = system.share_knowledge(
            name="Test Knowledge",
            description="Test description",
            knowledge_type=KnowledgeType.SKILL,
            content={"data": "test"},
            source_system="test"
        )
        
        assert package_id is not None
    
    def test_recommendations(self):
        """Test getting recommendations"""
        from openclaw_self_learning.systems.collective_intelligence import KnowledgeType
        
        system = CollectiveIntelligenceSystem(
            agent_id="test-agent",
            user_id="test-user",
            agent_name="Test Agent"
        )
        
        # Share some knowledge first
        system.share_knowledge(
            name="Test Knowledge",
            description="Test",
            knowledge_type=KnowledgeType.SKILL,
            content={},
            source_system="test"
        )
        
        recommendations = system.get_recommendations()
        assert isinstance(recommendations, list)


class TestConfiguration:
    """Tests for configuration"""
    
    def test_config_creation(self):
        """Test configuration creation"""
        config = SelfLearningConfig()
        
        assert config.plan_mode is not None
        assert config.auto_review is not None
        assert config.nudge is not None
    
    def test_config_dict_conversion(self):
        """Test config to dict conversion"""
        config = SelfLearningConfig()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert 'plan_mode' in config_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
