"""OffStar - Autonomous AI Agent for Decentralized Computing"""

from .core import OffStarCore
from .plugins import OffStarPlugin
from .task_engine import TaskEngine, Task
from .health_monitor import HealthMonitor

__version__ = "1.0.0"
__author__ = "OffStar Development Team"
__email__ = "dev@offstar.ai"

__all__ = [
    "OffStarCore",
    "OffStarPlugin",
    "TaskEngine",
    "Task",
    "HealthMonitor"
]