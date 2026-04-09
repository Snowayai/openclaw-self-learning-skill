"""
Collective Intelligence System

Multi-agent knowledge sharing and discovery.
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

# Knowledge type enum (fallback if full system not available)
class KnowledgeType(Enum):
    SKILL = "skill"
    MEMORY = "memory"
    STRATEGY = "strategy"
    WORKFLOW = "workflow"
    PREFERENCE = "preference"

# Try to import from full system
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "collective-intelligence-system"))
    from collective_intelligence_system import CollectiveIntelligenceManager
    FULL_SYSTEM_AVAILABLE = True
except ImportError:
    FULL_SYSTEM_AVAILABLE = False


class CollectiveIntelligenceSystem:
    """Collective Intelligence System for knowledge sharing"""
    
    def __init__(
        self,
        config=None,
        data_dir: Optional[str] = None,
        agent_id: Optional[str] = None,
        user_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        capabilities: Optional[List[str]] = None
    ):
        self.config = config
        self.data_dir = data_dir
        self.agent_id = agent_id
        self.user_id = user_id
        self.agent_name = agent_name
        self.capabilities = capabilities or []
        
        # In-memory storage for demo
        self._packages = []
        self._imports = []
        
        if FULL_SYSTEM_AVAILABLE:
            try:
                from collective_intelligence_system.types import AgentIdentity
                from collective_intelligence_system.core import CollectiveIntelligenceManagerConfig
                from collective_intelligence_system.types import CollectiveIntelligenceConfig as FullCIConfig
                
                agent = AgentIdentity(
                    agent_id=agent_id or "default",
                    user_id=user_id or "default",
                    agent_name=agent_name or "Default Agent",
                    agent_type="general"
                )
                ci_config = FullCIConfig() if config is None else config
                wrapped_config = CollectiveIntelligenceManagerConfig(
                    ci_config=ci_config,
                    current_agent=agent
                )
                self._manager = CollectiveIntelligenceManager(wrapped_config)
            except Exception as e:
                print(f"Warning: Could not initialize full CI system: {e}")
                self._manager = None
        else:
            self._manager = None
    
    def share_knowledge(
        self,
        name: str,
        description: str,
        knowledge_type: Any,
        content: Dict[str, Any],
        source_system: str,
        tags: Optional[List[str]] = None
    ) -> Optional[str]:
        """Share knowledge to collective intelligence"""
        if self._manager:
            return self._manager.share_knowledge(
                name=name,
                description=description,
                knowledge_type=knowledge_type,
                content=content,
                source_system=source_system,
                tags=tags
            )
        
        # Fallback: store locally
        package_id = f"pkg_{len(self._packages)}"
        self._packages.append({
            'id': package_id,
            'name': name,
            'description': description,
            'type': str(knowledge_type),
            'content': content,
            'source_system': source_system,
            'tags': tags or [],
            'agent_id': self.agent_id,
            'user_id': self.user_id,
            'created_at': datetime.now()
        })
        
        print(f"📤 Shared knowledge: {name}")
        return package_id
    
    def import_knowledge(self, package_id: str) -> bool:
        """Import knowledge from collective intelligence"""
        if self._manager:
            result = self._manager.import_knowledge(package_id)
            return result is not None
        
        # Fallback: find in local storage
        for pkg in self._packages:
            if pkg['id'] == package_id:
                self._imports.append({
                    'package_id': package_id,
                    'imported_at': datetime.now()
                })
                print(f"📥 Imported knowledge: {pkg['name']}")
                return True
        
        return False
    
    def get_recommendations(
        self,
        context: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get knowledge recommendations"""
        if self._manager:
            return self._manager.get_recommendations(context, limit)
        
        # Fallback: return available packages
        recommendations = []
        for pkg in self._packages:
            # Skip own packages
            if pkg.get('agent_id') == self.agent_id:
                continue
            
            recommendations.append({
                'package_id': pkg['id'],
                'name': pkg['name'],
                'type': pkg['type'],
                'reason': f"Shared by {pkg.get('agent_id', 'unknown')}",
                'score': 0.8
            })
        
        return recommendations[:limit]
    
    def get_report(self) -> Any:
        """Get collective intelligence report"""
        if self._manager:
            return self._manager.get_report()
        
        # Fallback: simple report
        my_packages = [p for p in self._packages if p.get('agent_id') == self.agent_id]
        
        return type('Report', (), {
            'my_shared_packages': len(my_packages),
            'my_total_shares': len(my_packages),
            'my_average_rating': 0.0,
            'my_imported_packages': len(self._imports),
            'my_successful_imports': len(self._imports),
            'recommended_packages': [],
            'insights': [
                f"You have shared {len(my_packages)} knowledge packages",
                f"You have imported {len(self._imports)} packages from others"
            ],
            'to_markdown': lambda: f"""
# Collective Intelligence Report

**Your Contributions:**
- Shared packages: {len(my_packages)}
- Total shares: {len(my_packages)}

**Your Learning:**
- Imported packages: {len(self._imports)}
- Successfully applied: {len(self._imports)}

**Insights:**
{chr(10).join(['- ' + i for i in [
    f"You have shared {len(my_packages)} knowledge packages",
    f"You have imported {len(self._imports)} packages from others"
]])}
            """
        })()


# Minimal config class
class CollectiveIntelligenceManagerConfig:
    def __init__(self, ci_config=None, current_agent=None):
        self.ci_config = ci_config
        self.current_agent = current_agent
