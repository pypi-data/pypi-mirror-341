
import asyncio
import weakref
import traceback
from typing import Coroutine, AsyncGenerator
import uuid

from toolbox51 import logger, SingletonMeta


from .operation import AsyncOperation
from .resource import AsyncResource
from . import exceptions


class PlaceHolder:
    def __new__(cls, *args, **kwargs):
        raise TypeError("占位符，不可实例化")

class Manager(metaclass=SingletonMeta):
    """
    一个外部请求为一个Operation，与Asyncio.Task进行区分。一般而言一个op为一个fast_api请求。
    一个op可以包含多个task，由task_manager.create_task在op中创建task。
    not thread-safe，不可用于多线程内部。
    只可用于默认事件循环的管理，不可以用户新建事件循环的内部管理。
    """
    
    _ops: dict[str, AsyncOperation] # [uuid, operation]
    _ops_lock: asyncio.Lock
    
    _resources: dict[str, AsyncResource] # [name, resource]
    _resources_lock: asyncio.Lock
    
    _task_index: weakref.WeakKeyDictionary[asyncio.Task, str] # [task_id, uuid]      使用 WeakKeyDictionary 来避免内存泄漏
    _task_index_lock: asyncio.Lock
    
    _default_priority: int
    
    def __init__(self):
        self._ops = {}
        self._ops_lock = asyncio.Lock()
        self._resources = {}
        self._resources_lock = asyncio.Lock()
        self._task_index = weakref.WeakKeyDictionary()
        self._task_index_lock = asyncio.Lock()
        
        self._default_priority = 10 # NOTE: 临时指定，默认优先级为10
    
    def set_default_priority(self, priority:int):
        self._default_priority = priority
    
    注册与删除: PlaceHolder
    
    async def register(
        self, id:uuid.UUID|str, 
        *,
        task:asyncio.Task|None = None, priority:int|None = None, clear_finished_ops:bool = True, 
    ) -> bool:
        """注册op"""
        try:
            if clear_finished_ops and not await self.clear_finished_ops():
                return False
            
            op_id = await self._get_op_id(id)
            op = AsyncOperation(op_id, priority or self._default_priority)
            await op.initialize()
            
            # 注册op
            async with self._ops_lock: 
                if op_id in self._ops:
                    raise exceptions.DuplicatedOperationID(f"重复的uuid: {op_id}")
                self._ops[op_id] = op
                
            if task is None:
                # 获取当前task
                if (task := asyncio.current_task()) is None:
                    raise exceptions.InvalidTask("无法获得当前task")
            # 将task注册到op中
            return await self._register_task_to_op(task, op_id, op)
            if (_op_id := self._task_index.get(task, None)) is not None and _op_id:
                if _op_id != op_id:
                    logger.warning("发现重复的task，不确定是否为bug，待验证。放弃注册task。")
                    return False
                else:
                    logger.info(f"task已经存在于操作[{op_id}]中，不需要重复注册")
                    return True
            await op.register(task)
            async with self._task_index_lock:
                if task in self._task_index:
                    logger.warning("发现重复的task，不确定是否为bug，待验证。仍然注册task。")
                self._task_index[task] = op_id
                    
            return True
        except Exception as e:
            logger.warning(f"注册操作失败: {e}")
            traceback.print_exc()
            return False
        
    async def register_task(
        self, id:uuid.UUID|str, 
        *,
        task:asyncio.Task|None = None, 
    ):
        """注册task"""
        try:
            if task is None:
                # 获取当前task
                if (task := asyncio.current_task()) is None:
                    raise exceptions.InvalidTask("无法获得当前task")
            op_id = await self._get_op_id(id)
            return await self._register_task_to_op(task, op_id)
            if (_op_id := self._task_index.get(task, None)) is not None and _op_id:
                if _op_id != op_id:
                    logger.warning("发现重复的task，不确定是否为bug，待验证。放弃注册task。")
                    return False
                else:
                    logger.info(f"task已经存在于操作[{op_id}]中，不需要重复注册")
                    return True
            op = await self._get_op(op_id)
            await op.register(task)
            async with self._task_index_lock:
                if task in self._task_index:
                    logger.warning("发现重复的task，不确定是否为bug，待验证。仍然注册task。")
                self._task_index[task] = op_id
            return True
        except Exception as e:
            logger.warning(f"注册task失败: {e}")
            traceback.print_exc()
            return False
        
    async def wrap_generator(
        self, id:uuid.UUID|str, generator:AsyncGenerator,
    ) -> AsyncGenerator:
        """注册generator"""
        try:
            await self.register_task(id, task=asyncio.current_task())
        except Exception as e:
            logger.warning(f"注册generator失败: {e}")
            traceback.print_exc()
            return
        try:
            async for item in generator:
                await self.check_terminate(id, check_suspend=False, silence=True, logger_stacklevel=3)
                yield item
        except exceptions.TerminatedSignal as e:
            logger.warning(f"generator被终止: {e}")
            return
            
        
    async def create_task(
        self, 
        coro:Coroutine,
    ) -> asyncio.Task|None:
        """
        新建task并注册，包装了asycio.create_task
        同时会进行check_terminate，所以也会抛出TerminatedSignal
        """
        try:
            op_id = await self._get_op_id()
            try:
                await self.check_terminate(op_id)
            except exceptions.TerminatedSignal as e:
                logger.warning(f"尝试在操作[{op_id}]中新建task，但操作[{op_id}]已被终止")
                raise e
            task = asyncio.create_task(coro)
            
            # 将task注册到manager中
            async with self._task_index_lock:
                if task in self._task_index:
                    logger.warning("发现重复的task，不确定是否为bug，待验证")
                self._task_index[task] = op_id
                
            # 将task注册到op中
            op = await self._get_op(op_id)
            await op.register(task)
            
            return task
        except exceptions.TerminatedSignal as e:
            raise e
        except Exception as e:
            logger.warning(f"新建task失败: {e}")
            traceback.print_exc()
            return None
    
    async def clear_finished_ops(
        self,
    ) -> bool:
        """清除已完成的op"""
        try:
            # 清理所有op中已完成的task，并找出已完成的op
            op_ids_to_clear = []
            async with self._ops_lock:
                for op_id, op in self._ops.items():
                    if await op.is_finished():
                        op_ids_to_clear.append(op_id)
            # 清理已完成的op
            for op_id in op_ids_to_clear:
                async with self._ops_lock:
                    if op_id in self._ops:
                        self._ops.pop(op_id)
            return True
        except Exception as e:
            logger.warning(f"清除已完成的op失败: {e}")
            traceback.print_exc()
            return False
                
        
    
    
    外部操作: PlaceHolder
    
    async def terminate(
        self, 
        id:uuid.UUID|str, 
        *,
        timeout = 0,
        clear_finished_ops:bool = True, 
    ) -> bool:
        """终止op"""
        try:
            op = await self._get_op(id)
            await op.terminate(timeout=timeout)
            if clear_finished_ops and not await self.clear_finished_ops():
                return False
            return True
        except exceptions.UnregisteredOperation:
            logger.warning(f"操作[{id}]未注册或已结束")
            return False
        except Exception as e:
            logger.warning(f"终止操作失败: {e}")
            traceback.print_exc()
            return False
        
    async def kill(
        self, 
        id:uuid.UUID|str,
        clear_finished_ops:bool = True, 
    ) -> bool:
        """强制终止op"""
        try:
            op = await self._get_op(id)
            await op.kill_all()
            if clear_finished_ops and not await self.clear_finished_ops():
                return False
            return True
        except exceptions.UnregisteredOperation:
            logger.warning(f"操作[{id}]未注册或已结束")
            return False
        except Exception as e:
            logger.warning(f"强制终止操作失败: {e}")
            traceback.print_exc()
            return False
        
    async def suspend(
        self, 
        id:uuid.UUID|str,
    ) -> bool:
        """挂起op"""
        try:
            op = await self._get_op(id)
            await op.suspend()
            return True
        except exceptions.UnregisteredOperation:
            logger.warning(f"操作[{id}]未注册或已结束")
            return False
        except Exception as e:
            logger.warning(f"挂起操作失败: {e}")
            traceback.print_exc()
            return False
        
    async def resume(
        self, 
        id:uuid.UUID|str,
    ) -> bool:
        """恢复op"""
        try:
            op = await self._get_op(id)
            await op.resume()
            return True
        except exceptions.UnregisteredOperation:
            logger.warning(f"操作[{id}]未注册或已结束")
            return False
        except Exception as e:
            logger.warning(f"恢复操作失败: {e}")
            traceback.print_exc()
            return False
            
    
    
    状态检查: PlaceHolder
    
    async def check_terminate(
        self, 
        id: uuid.UUID|str|None = None,
        check_suspend: bool = True,
        silence: bool = False,
        logger_stacklevel: int = 2,
    ) -> bool:
        """
        检查任务是否需要终止或挂起
        # Params
            - id: 操作ID，可以是UUID、字符串或None(表示当前任务)
            - check_suspend: 是否检查挂起状态
            - silence: 是否静默模式，静默模式下仅在遇到外部操作时输出日志
            - logger_stacklevel: 日志堆栈层级
        # Returns
            - bool: False表示检查失败
        # Exceptions
            - TerminatedSignal: 表示需要终止操作
        ---
        逻辑:
        - 正常状态: 返回True
        - 查询到终止信号: 抛出TerminatedSignal
        - 查询到挂起信号: 挂起直到恢复
        - 未注册的task: 说明是未被管理的野task，返回False，不抛出异常
        - 未注册的op: 说明传入id且id有误，或未传入id且成功找到已注册的task，抛出TerminalSignal
        - 其他异常: 返回False，不抛出异常
        """
        if not silence:
            logger.info("检查操作状态...", stacklevel=logger_stacklevel)
        try:
            op = await self._get_op(id)
        
            # 检查是否需要终止任务
            if op.event_terminate.is_set():
                logger.info(f"检测到操作[{op.id}]的终止事件")
                raise exceptions.TerminatedSignal(f"操作[{op.id}]需要被终止")
            # 检查是否需要挂起/恢复任务
            flag = False
            if check_suspend:
                if flag := not op.event_run.is_set():
                    logger.info(f"操作[{op.id}]已被挂起")
                await op.event_run.wait()
            if flag:
                logger.info(f"操作[{op.id}]已从挂起恢复")
            elif not silence:
                logger.info(f"操作[{op.id}]正常运行")
            
            return True
        except exceptions.UnregisteredTask as e:
            if not silence:
                logger.warning(f"当前task未注册: {e}")
            return False
        except exceptions.UnregisteredOperation as e:
            logger.warning(f"操作[{id}]未注册或已结束，尝试终止任务: {e}")
            raise exceptions.TerminatedSignal(f"操作[{id}]未注册或已结束，尝试终止任务")
        except exceptions.TerminatedSignal as e:
            raise e
        except Exception as e:
            logger.error(f"疑似发生协程管理错误或内存泄漏，请尽快排查: {e}")
            traceback.print_exc()
            return False

    
    资源操作: PlaceHolder
    
    async def touch_resource(
        self, 
        name: str, 
        *,
        parallel: int|None = None,
    ) -> bool:
        """检查或注册资源"""
        try:
            # 注册资源
            async with self._resources_lock:
                if (resource := self._resources.get(name, None)) is not None:
                    if parallel is not None and resource.parallel == parallel:
                        logger.info(f"资源[{name}]已存在，并行数: {parallel}, 剩余资源数: {resource.resources_left}")
                        return True
                    raise exceptions.DuplicatedResource(f"资源[{name}]已存在，且并行数冲突: self={resource.parallel}, new={parallel}")
                resource = AsyncResource(name, parallel or 1, default_priority=self._default_priority)
                await resource.initialize()
                self._resources[name] = resource
            return True
        except Exception as e:
            logger.warning(f"注册操作失败: {e}")
            traceback.print_exc()
            return False
        
    async def register_resource(
        self,
        name: str,
        *,
        parallel: int = 1,
    ) -> bool:
        """注册资源"""
        try:
            # 注册资源
            async with self._resources_lock:
                if name in self._resources:
                    raise exceptions.DuplicatedResource(f"资源[{name}]已存在")
                resource = AsyncResource(name, parallel, default_priority=self._default_priority)
                await resource.initialize()
                self._resources[name] = resource
            return True
        except Exception as e:
            logger.warning(f"注册操作失败: {e}")
            traceback.print_exc()
            return False
    
    async def allocate(
        self, 
        resource:str,
        *,
        priority:int|None = None,
    ) -> asyncio.Event|None:
        """
        分配资源
        """
        try:
            async with self._resources_lock:
                if resource not in self._resources:
                    raise exceptions.InvalidResource(f"资源[{resource}]不存在")
                resource_instance = self._resources[resource]
            op = None
            try:
                op = await self._get_op()
            except exceptions.UnregisteredTask as e:
                logger.warning(f"当前task未注册: {e}")
            except exceptions.UnregisteredOperation as e:
                logger.warning(f"当前task未注册: {e}")
            return await resource_instance.allocate(op, priority)
        except Exception as e:
            logger.warning(f"分配资源失败: {e}")
            traceback.print_exc()
            return None
        
    async def release(
        self, 
        resource:str,
    ) -> bool:
        """释放资源"""
        try:
            async with self._resources_lock:
                if resource not in self._resources:
                    raise exceptions.InvalidResource(f"资源[{resource}]不存在")
                resource_instance = self._resources[resource]
            await resource_instance.release()
            return True
        except Exception as e:
            logger.warning(f"释放资源失败: {e}")
            traceback.print_exc()
            return False
    
    
    private: PlaceHolder
    
    async def _get_current_task(self) -> asyncio.Task:
        """获取当前task，并验证是否已注册"""
        if (task := asyncio.current_task()) is None:
            raise exceptions.InvalidTask("无法获得当前task")
        async with self._task_index_lock:
            if task not in self._task_index:
                raise exceptions.UnregisteredTask(f"task[{id(task)}]未在manager中注册")
        return task
    
    async def _get_op_id(self, id:uuid.UUID|str|None=None) -> str:
        """获取op_id"""
        if id:
            return str(id)
        task = await self._get_current_task()
        async with self._task_index_lock:
            op_id = self._task_index[task]
        return op_id
    
    async def _get_op(self, id:uuid.UUID|str|None=None) -> AsyncOperation:
        op_id = await self._get_op_id(id)
        async with self._ops_lock:
            if op_id not in self._ops:
                raise exceptions.UnregisteredOperation(f"操作[{op_id}]未在manager中注册")
            op = self._ops[op_id]
        return op
    
    async def _pop_op(self, id:uuid.UUID|str|None=None) -> AsyncOperation:
        op_id = await self._get_op_id(id)
        async with self._ops_lock:
            if op_id not in self._ops:
                raise exceptions.UnregisteredOperation(f"操作[{op_id}]未在manager中注册")
            op = self._ops.pop(op_id)
        return op
    
    async def _register_task_to_op(self, task:asyncio.Task, op_id:str, op:AsyncOperation|None=None) -> bool:
        if (_op_id := self._task_index.get(task, None)) is not None and _op_id:
            if _op_id != op_id:
                logger.warning("发现重复的task，不确定是否为bug，待验证。放弃注册task。")
                return False
            else:
                logger.info(f"task已经存在于操作[{op_id}]中，不需要重复注册")
                return True
        if op is None:
            op = await self._get_op(op_id)
        await op.register(task)
        async with self._task_index_lock:
            if task in self._task_index:
                logger.warning("发现重复的task，不确定是否为bug，待验证。仍然注册task。")
            self._task_index[task] = op_id
        return True

manager = Manager()