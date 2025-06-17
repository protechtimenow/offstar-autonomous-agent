# AsyncTaskProcessor - Core task execution engine
import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class Task:
    id: str
    type: str
    params: Dict[str, Any]
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    result: Dict[str, Any] = None
    error: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.id is None:
            self.id = str(uuid.uuid4())

class AsyncTaskProcessor:
    """
    Core async task processing engine for OffStar
    Handles task scheduling, execution, and monitoring
    """
    
    def __init__(self, max_concurrent_tasks: int = 10):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.active_tasks: Dict[str, Task] = {}
        self.completed_tasks: Dict[str, Task] = {}
        self.plugin_registry = {}
        self.running = False
        self.worker_tasks: List[asyncio.Task] = []
        
    async def register_plugin(self, name: str, plugin):
        """Register a plugin for task processing"""
        self.plugin_registry[name] = plugin
        await plugin.initialize()
        
    async def submit_task(self, task_type: str, params: Dict[str, Any], 
                         priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Submit a new task for processing"""
        task = Task(
            id=str(uuid.uuid4()),
            type=task_type,
            params=params,
            priority=priority
        )
        
        # Priority queue uses negative values for max-heap behavior
        await self.task_queue.put((-priority.value, task.created_at, task))
        return task.id
    
    async def start_processing(self):
        """Start the task processing workers"""
        self.running = True
        
        # Start worker coroutines
        for i in range(self.max_concurrent_tasks):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.worker_tasks.append(worker)
            
        await asyncio.gather(*self.worker_tasks)
    
    async def stop_processing(self):
        """Stop all task processing"""
        self.running = False
        
        # Cancel all worker tasks
        for worker in self.worker_tasks:
            worker.cancel()
            
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()
    
    async def _worker(self, worker_id: str):
        """Worker coroutine that processes tasks from the queue"""
        while self.running:
            try:
                # Wait for task with timeout to allow periodic checks
                try:
                    _, _, task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                    
                # Execute the task
                await self._execute_task(task, worker_id)
                
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
    
    async def _execute_task(self, task: Task, worker_id: str):
        """Execute a single task"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        self.active_tasks[task.id] = task
        
        try:
            # Find appropriate plugin
            plugin = self._find_plugin_for_task(task.type)
            if not plugin:
                raise ValueError(f"No plugin found for task type: {task.type}")
            
            # Execute task
            if task.type == "defi_metrics":
                result = await plugin.fetch_protocol_metrics(task.params.get('protocol'))
                task.result = {
                    'tvl': float(result.tvl),
                    'volume_24h': float(result.volume_24h),
                    'apy': float(result.apy),
                    'risk_score': result.risk_score,
                    'timestamp': result.timestamp.isoformat()
                }
            elif task.type == "yield_optimization":
                result = await plugin.calculate_yield_opportunities()
                task.result = {'opportunities': result}
            elif task.type == "health_check":
                result = await plugin.monitor_health()
                task.result = result
            else:
                raise ValueError(f"Unknown task type: {task.type}")
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
        
        finally:
            # Move from active to completed
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
            self.completed_tasks[task.id] = task
    
    def _find_plugin_for_task(self, task_type: str):
        """Find the appropriate plugin for a task type"""
        # Simple mapping - could be made more sophisticated
        if task_type in ['defi_metrics', 'yield_optimization', 'health_check']:
            return self.plugin_registry.get('defi')
        return None
    
    async def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get the status of a specific task"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
        elif task_id in self.completed_tasks:
            task = self.completed_tasks[task_id]
        else:
            return None
            
        return {
            'id': task.id,
            'type': task.type,
            'status': task.status.value,
            'priority': task.priority.value,
            'created_at': task.created_at.isoformat(),
            'started_at': task.started_at.isoformat() if task.started_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'result': task.result,
            'error': task.error
        }
    
    async def get_system_metrics(self) -> Dict:
        """Get overall system metrics"""
        return {
            'active_tasks': len(self.active_tasks),
            'queued_tasks': self.task_queue.qsize(),
            'completed_tasks': len(self.completed_tasks),
            'max_concurrent': self.max_concurrent_tasks,
            'running': self.running,
            'plugins_registered': len(self.plugin_registry)
        }