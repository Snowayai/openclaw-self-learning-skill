"""
CLI interface for OpenClaw Self-Learning Suite
"""
import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="OpenClaw Self-Learning Suite CLI",
        prog="openclaw-self-learning"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize configuration")
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing configuration"
    )
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show system status")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    # Example command
    example_parser = subparsers.add_parser("example", help="Run example")
    example_parser.add_argument(
        "type",
        choices=["basic", "skill"],
        default="basic",
        help="Example type"
    )
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_config(force=args.force)
    elif args.command == "status":
        show_status()
    elif args.command == "test":
        run_tests(verbose=args.verbose)
    elif args.command == "example":
        run_example(args.type)
    else:
        parser.print_help()


def init_config(force=False):
    """Initialize configuration"""
    from openclaw_self_learning import SelfLearningConfig
    
    config_path = Path.home() / ".openclaw" / "self_learning.yaml"
    
    if config_path.exists() and not force:
        print(f"⚠️  Configuration already exists at {config_path}")
        print("Use --force to overwrite")
        return
    
    config = SelfLearningConfig()
    config.to_file(str(config_path))
    print(f"✅ Configuration created at {config_path}")


def show_status():
    """Show system status"""
    from openclaw_self_learning import SelfLearningConfig
    
    config = SelfLearningConfig().load_or_create_default()
    
    print("📊 OpenClaw Self-Learning Suite Status")
    print("=" * 50)
    
    systems = [
        ("Plan Mode", config.plan_mode.enabled),
        ("Auto-Review", config.auto_review.enabled),
        ("Nudge System", config.nudge.enabled),
        ("Skill Evolution", config.skill_evolution.enabled),
        ("Meta-Learning", config.meta_learning.enabled),
        ("Collective Intelligence", config.collective_intelligence.enabled),
    ]
    
    for name, enabled in systems:
        status = "✅" if enabled else "❌"
        print(f"{status} {name}")
    
    print("=" * 50)


def run_tests(verbose=False):
    """Run tests"""
    import subprocess
    
    args = ["pytest", "tests/"]
    if verbose:
        args.append("-v")
    
    result = subprocess.run(args)
    sys.exit(result.returncode)


def run_example(example_type="basic"):
    """Run example"""
    import subprocess
    
    examples = {
        "basic": "examples/basic_example.py",
        "skill": "examples/skill_integration_example.py"
    }
    
    if example_type not in examples:
        print(f"❌ Unknown example type: {example_type}")
        return
    
    script = examples[example_type]
    result = subprocess.run([sys.executable, script])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
