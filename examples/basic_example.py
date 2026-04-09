"""
Basic Example: Using Self-Learning Agent

This example demonstrates how to use the Self-Learning Agent
with all six learning systems integrated.
"""
from openclaw_self_learning import SelfLearningAgent


def main():
    # Create a self-learning agent
    print("🚀 Creating Self-Learning Agent...\n")
    
    agent = SelfLearningAgent(
        agent_id="demo-agent",
        user_id="demo-user",
        name="Demo Learning Agent",
        capabilities=["coding", "analysis", "planning"]
    )
    
    print(f"✅ Agent created: {agent.name}")
    print(f"   ID: {agent.agent_id}")
    print(f"   Capabilities: {', '.join(agent.capabilities)}\n")
    
    # Example 1: Simple task processing
    print("=" * 60)
    print("Example 1: Simple Task")
    print("=" * 60)
    
    response = agent.process("Help me debug this Python error")
    print(f"\nUser: Help me debug this Python error")
    print(f"Agent: {response.get('content')}")
    
    if response.get('strategy_used'):
        print(f"Strategy: {response['strategy_used']}")
    
    # Example 2: Task requiring plan confirmation
    print("\n" + "=" * 60)
    print("Example 2: Complex Task (Plan Mode)")
    print("=" * 60)
    
    response = agent.process("Create a complete user authentication system")
    
    if response.get('requires_confirmation'):
        print("\n📋 Plan generated (requires confirmation):")
        print(response['plan'])
        
        # Simulate user confirmation
        print("\n✅ User confirmed the plan")
        response = agent.confirm_plan(response['session_id'], confirmed=True)
    
    print(f"\nResult: {response.get('content')}")
    
    # Example 3: Knowledge discovery
    print("\n" + "=" * 60)
    print("Example 3: Knowledge Discovery")
    print("=" * 60)
    
    recommendations = agent.discover_knowledge(context="debugging")
    print(f"\n🔍 Found {len(recommendations)} relevant knowledge packages:")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['name']}")
        print(f"   Type: {rec['type']}")
        print(f"   Why: {rec['reason']}")
    
    # Example 4: Generate learning report
    print("\n" + "=" * 60)
    print("Example 4: Learning Report")
    print("=" * 60)
    
    report = agent.get_learning_report()
    print("\n" + report)
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
