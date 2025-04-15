
import asyncio
import itertools

from toolbox51 import logger

from .operation import AsyncOperation

class AsyncResource:
    """
    需要使用initialize初始化资源。
    注意只能在同一个事件循环中管理资源。
    """
    name: str
    
    pq: asyncio.PriorityQueue
    pq_count: itertools.count
    
    parallel: int
    resources_left: int
    
    lock: asyncio.Lock
    event_ready: asyncio.Event # 用于通知资源可用，resources_left为0时clear，大于0时set
    event_allocate: asyncio.Event # 用于通知有任务申请资源，allocate时set，pq搬空时clear
    
    default_priority: int
    
    _initialized: bool
    
    @property
    def initialized(self) -> bool:
        return self._initialized
    
    def __init__(self, name:str, parallel:int, default_priority:int=10, in_coro=True):
        logger.info(f"创建资源[{name}], {parallel=}, {default_priority=}")
        self.name = name
        
        self.pq = asyncio.PriorityQueue()
        self.pq_count = itertools.count()
        
        self.parallel = parallel
        self.resources_left = parallel
        
        self.lock = asyncio.Lock()
        self.event_ready = asyncio.Event()
        self.event_ready.set()
        self.event_allocate = asyncio.Event()
        
        self.default_priority = default_priority
        
        if in_coro:
            asyncio.create_task(self.round_robin())
        self._initialized = in_coro
        
    
    async def initialize(self):
        """启动轮询"""
        async with self.lock:
            if not self.initialized:
                asyncio.create_task(self.round_robin())
                self._initialized = True
            
    
    async def allocate(self, op:AsyncOperation|None=None, priority:int|None=None) -> asyncio.Event:
        """
        为op申请资源。
        申请资源是一次性的。如果op中有两个task，均需要使用资源，则需要分别申请。
        申请资源后获得一个event，需要await event后即可使用资源，使用后需release。
        """
        await self.initialize()
        if priority is None:
            if op is None:
                priority = self.default_priority
            else:
                priority = op.priority
        async with self.lock:
            event = asyncio.Event()
            await self.pq.put((priority, next(self.pq_count), op, event))
            self.event_allocate.set()
            return event
        
    async def release(self):
        await self.initialize()
        async with self.lock:
            self.resources_left += 1
            self.event_ready.set()
        
    async def round_robin(self):
        while(True):
            # 如果优先级队列为空，则等待新资源申请
            if self.pq.empty():
                self.pq_count = itertools.count()
                logger.debug(f"资源[{self.name}]队列已清空，等待新的资源申请")
                await self.event_allocate.wait()
            # 等待可用资源
            await self.event_ready.wait()
            # 取用资源
            async with self.lock:
                # 再次检查队列是否为空
                if self.pq.empty():
                    continue
                op: AsyncOperation|None
                event: asyncio.Event
                # pop
                priority, _, op, event = await self.pq.get()
                if op is not None: # 已注册的操作
                    # 检查操作是否被挂起
                    if not op.event_run.is_set():
                        logger.debug(f"操作[{op.id}]被挂起，跳过")
                        await self.pq.put((priority, next(self.pq_count), op, event))
                        continue
                    # 检查操作是否已终止
                    if op.event_terminate.is_set():
                        logger.debug(f"操作[{op.id}]已终止，移除")
                        continue
                    # 资源分配
                    logger.debug(f"将资源[{self.name}]分配给操作[{op.id}]")
                else:
                    logger.debug(f"将资源[{self.name}]分配给未注册操作")
                if self.resources_left <= 0:
                    raise AssertionError("resources_left不大于0时理应无法到达这里")
                self.resources_left -= 1
                if self.resources_left == 0:
                    self.event_ready.clear()
                # 通知操作已获得资源
                event.set()
                # 如果队列已经为空，则复位event_allocate
                if self.pq.empty():
                    self.event_allocate.clear()
        assert False, "unreachable"