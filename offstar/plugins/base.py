"""Base plugin interface for OffStar"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any

class OffStarPlugin(ABC):
    """
    Base class for all OffStar plugins
    
    Provides common functionality and interface for plugin development
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.status = "initialized"
        self.last_health_check = None
        self.errors = []
        self.metrics = {
            "tasks_executed": 0,
            "errors_count": 0,
            "avg_execution_time": 0.0
        }
    
    async def initialize(self) -> bool:
        """
        Initialize the plugin
        
        Returns:
            bool: True if initialization successful
        """
        try:
            await self._setup()
            self.status = "ready"
            return True
        except Exception as e:
            self.status = "failed"
            self.errors.append(f"Initialization error: {str(e)}")
            return False
    
    @abstractmethod
    async def execute(self, task: Any) -> Dict:
        """
        Core plugin execution method
        
        Args:
            task: Task to execute
            
        Returns:
            Dict: Execution result
        """
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> List[str]:
        """
        Declare plugin capabilities
        
        Returns:
            List[str]: List of capability identifiers
        """
        pass
    
    async def health_check(self) -> Dict:
        """
        Plugin self-diagnostics
        
        Returns:
            Dict: Health status information
        """
        self.last_health_check = datetime.now()
        
        status = "healthy"
        if len(self.errors) > 0:
            status = "degraded"
        if self.status == "failed":
            status = "failed"
            
        return {
            "name": self.name,
            "version": self.version,
            "status": status,
            "last_check": self.last_health_check.isoformat(),
            "error_count": len(self.errors),
            "recent_errors": self.errors[-5:] if self.errors else [],
            "metrics": self.metrics
        }
    
    async def _setup(self):
        """
        Plugin-specific setup logic
        
        Override in subclasses for initialization
        """
        pass
    
    def _log_error(self, error: str):
        """
        Log an error for health monitoring
        
        Args:
            error: Error message to log
        """
        self.errors.append(f"{datetime.now().isoformat()}: {error}")
        self.metrics["errors_count"] += 1
        
        # Keep only last 100 errors
        if len(self.errors) > 100:
            self.errors = self.errors[-100:]
    
    def _update_metrics(self, execution_time: float):
        """
        Update execution metrics
        
        Args:
            execution_time: Task execution time in seconds
        """
        self.metrics["tasks_executed"] += 1
        
        # Update average execution time
        current_avg = self.metrics["avg_execution_time"]
        task_count = self.metrics["tasks_executed"]
        
        new_avg = ((current_avg * (task_count - 1)) + execution_time) / task_count
        self.metrics["avg_execution_time"] = new_avg