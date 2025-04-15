

import asyncio
import weakref

from toolbox51 import logger

class AsyncOperation:
    """
    异常由TaskManager处理。
    """
    id: str
    priority: int
    task_refs: list[weakref.ref[asyncio.Task]]
    
    lock: asyncio.Lock
    event_terminate: asyncio.Event
    event_run: asyncio.Event
    
    
    def __init__(self, id:str, priority:int):
        self.id = id
        self.priority = priority
        self.task_refs = []
        
        self.lock = asyncio.Lock()
        self.event_terminate = asyncio.Event()
        self.event_run = asyncio.Event()
        self.event_run.set()
        
    
    async def initialize(self):
        ...
        
    
    async def register(self, task:asyncio.Task, clear_finished_tasks=False):
        async with self.lock:
            if clear_finished_tasks:
                await self._clear_finished_tasks()
            self.task_refs.append(weakref.ref(task))
        
    async def terminate(self, timeout:int=0):
        async with self.lock:
            logger.info(f"正在终止操作[{self.id}]...")
            self.event_terminate.set()
            logger.info(f"正在等待操作[{self.id}]中的任务安全结束...")
            # TODO: 后续考虑添加超时机制
            tasks:list[asyncio.Task] = [task for task_ref in self.task_refs if (task := task_ref()) is not None]
            if timeout:
                done, pending = await asyncio.wait(tasks, timeout=timeout)
                for p in pending:
                    logger.warning(f"任务[{id(p)}]未能安全结束，强制终止...有可能会导致资源调度出现问题")
                    p.cancel()
            else:
                await asyncio.gather(*tasks, return_exceptions=True) 
            logger.info(f"操作[{self.id}]已终止")
            
    async def kill_all(self):
        async with self.lock:
            logger.warning(f"正在强制终止操作[{self.id}]...")
            tasks:list[asyncio.Task] = [task for task_ref in self.task_refs if (task := task_ref()) is not None]
            for task in tasks:
                logger.warning(f"正在强制终止任务[{id(task)}]...有可能会导致资源调度出现问题")
                task.cancel()
            logger.warning(f"操作[{self.id}]已强制终止")
    
    async def suspend(self, clear_finished_tasks=False):
        async with self.lock:
            if clear_finished_tasks:
                await self._clear_finished_tasks()
            if self.event_run.is_set():
                logger.info(f"挂起操作[{self.id}]")
                self.event_run.clear()
            else:
                logger.info(f"操作[{self.id}]挂起中，无需重复挂起")
            
    async def resume(self, clear_finished_tasks=False):
        async with self.lock:
            if clear_finished_tasks:
                await self._clear_finished_tasks()
            if self.event_run.is_set():
                logger.info(f"操作[{self.id}]正常运行中，无需恢复")
            else:
                logger.info(f"恢复操作[{self.id}]")
                self.event_run.set()
                
    async def is_finished(self) -> bool:
        async with self.lock:
            await self._clear_finished_tasks()
            if not self.task_refs:
                return True
            else:
                return False
    
    async def _clear_finished_tasks(self):
        self.task_refs = [
            task_ref for task_ref in self.task_refs if (task := task_ref()) is not None and not task.done()
        ]