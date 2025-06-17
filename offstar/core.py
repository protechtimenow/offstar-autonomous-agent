"""OffStar Core - Main agent orchestration system"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid
import json

class OffStarCore:
    """
    Main OffStar agent orchestration system
    
    Coordinates autonomous operation across plugins, manages tasks,
    and interfaces with IO.NET for distributed computing.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.agent_id = str(uuid.uuid4())
        self.status = "initializing"
        self.start_time = datetime.now()
        
        # Plugin instances
        self.plugins: Dict[str, Any] = {}
        
    async def initialize(self) -> bool:
        """
        Bootstrap OffStar with R2D2-like resilience
        
        Returns:
            bool: True if initialization successful
        """
        try:
            self.status = "initializing"
            
            # Register core plugins
            await self._register_core_plugins()
            
            self.status = "ready"
            
            print(f"🤖 OffStar Agent {self.agent_id[:8]} initialized successfully")
            return True
            
        except Exception as e:
            self.status = "failed"
            print(f"❌ OffStar initialization failed: {e}")
            return False
    
    async def register_plugin(self, name: str, plugin: Any) -> bool:
        """
        Register a new plugin for hot-loading
        
        Args:
            name: Plugin identifier
            plugin: Plugin instance
            
        Returns:
            bool: True if registration successful
        """
        try:
            await plugin.initialize()
            self.plugins[name] = plugin
            
            print(f"🔌 Plugin '{name}' registered successfully")
            return True
            
        except Exception as e:
            print(f"❌ Plugin registration failed for '{name}': {e}")
            return False
    
    async def execute_task(self, task: Dict) -> Dict:
        """
        Execute a task through the appropriate plugin
        
        Args:
            task: Task to execute
            
        Returns:
            Dict: Task execution result
        """
        try:
            # Route task to appropriate plugin
            plugin_type = task.get('plugin_type')
            plugin = self.plugins.get(plugin_type)
            if not plugin:
                raise ValueError(f"Plugin '{plugin_type}' not found")
            
            # Execute task
            result = await plugin.execute(task)
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            return error_result
    
    async def run_forever(self):
        """
        Main operational loop - autonomous operation
        """
        print(f"🚀 OffStar Agent {self.agent_id[:8]} starting autonomous operation...")
        
        while self.status != "shutdown":
            try:
                # Brief pause (30-second operational cycle)
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"⚠️ Error in main loop: {e}")
                await asyncio.sleep(60)  # Longer pause on error
    
    async def shutdown(self):
        """
        Graceful shutdown of OffStar agent
        """
        print(f"🛑 Shutting down OffStar Agent {self.agent_id[:8]}...")
        
        self.status = "shutdown"
        
        print("✅ OffStar shutdown complete")
    
    async def get_status(self) -> Dict:
        """
        Get comprehensive agent status
        
        Returns:
            Dict: Complete status information
        """
        uptime = datetime.now() - self.start_time
        
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "uptime_seconds": uptime.total_seconds(),
            "plugins": list(self.plugins.keys()),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _register_core_plugins(self):
        """
        Register essential plugins
        """
        from .plugins.defi import DeFiPlugin
        
        # Register core plugins
        await self.register_plugin("defi", DeFiPlugin())