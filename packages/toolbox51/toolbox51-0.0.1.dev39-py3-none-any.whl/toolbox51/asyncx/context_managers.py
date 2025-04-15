
import asyncio
import contextlib
import traceback
import uuid
from toolbox51 import logger

from .manager import manager
from . import exceptions





@contextlib.asynccontextmanager
async def async_closing(agen):
    """确保异步生成器正确关闭"""
    try:
        yield agen
    finally:
        await agen.aclose()  # 确保异步关闭



class AllocateResource(contextlib.AbstractAsyncContextManager):
    """
    申请资源，并在退出时释放资源
    仅在当前op/task未注册时才使用priority
    # Exceptions
    - AllocateResourceFailed: 申请资源失败
    - ReleaseResourceFailed: 释放资源失败
    """
    
    resource: str
    priority: int|None
    
    validate: bool
    parallel: int|None = None
    
    event: asyncio.Event|None
    
    def __init__(
        self, 
        resource: str, 
        *, 
        url: str|None = None,
        priority: int|None = None,
        validate: bool = False, parallel: int|None = None, 
    ):
        if url is not None:
            resource = f"{resource}@{url}"
        self.resource = resource
        self.priority = priority
        self.validate = validate
        self.parallel = parallel
        self.event = None
        
    async def __aenter__(self) -> "AllocateResource":
        """申请资源"""
        
        if self.validate and not await manager.touch_resource(self.resource, parallel=self.parallel):
            raise exceptions.InvalidResource(f"Invalid resource: {self.resource}")
        
        await manager.check_terminate(logger_stacklevel=3) # 这里的异常直接往外抛
        self.event = await manager.allocate(self.resource, priority=self.priority)
        if self.event is None:
            raise exceptions.AllocateResourceFailed
        try:
            await self.event.wait()
            return self
        except Exception as e:
            logger.error(f"Allocate resource failed: {e}")
            traceback.print_exc()
            raise exceptions.AllocateResourceFailed
        
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """释放资源"""
        if self.event is not None and not await manager.release(self.resource):
            raise exceptions.ReleaseResourceFailed
        
    async def check_terminate(
        self, 
        id: uuid.UUID|str|None = None,
        check_suspend: bool = True,
        silence: bool = False,
        logger_stacklevel: int = 2,
    ) -> bool:
        """
        检查任务是否需要终止或挂起
        如果遇到挂起事件，则需要围绕挂起进行资源管理（先释放资源，恢复时再申请资源）
        请勿在流式调用中检查挂起，否则可能无法恢复。
        """
        if not silence:
            logger.info("检查操作状态...", stacklevel=logger_stacklevel)
        try:
            op = await manager._get_op(id)
        
            # 检查是否需要终止任务
            if op.event_terminate.is_set():
                logger.info(f"检测到操作[{op.id}]的终止事件")
                raise exceptions.TerminatedSignal(f"操作[{op.id}]需要被终止") 
                # NOTE: 此时释放资源由上下文管理器调用__aexit__完成，无需手动释放
                
            # 检查是否需要挂起/恢复任务
            flag = False
            if check_suspend:
                if flag := not op.event_run.is_set():
                    # 检测到挂起，释放资源
                    logger.info(f"操作[{op.id}]试图挂起，正在释放资源...")
                    if self.event is not None and not await manager.release(self.resource):
                        raise exceptions.ReleaseResourceFailed
                    self.event = None
                    logger.info(f"操作[{op.id}]已被挂起")
                await op.event_run.wait()
            if flag:
                # 从挂起恢复，重新申请资源
                logger.info(f"操作[{op.id}]试图从挂起中恢复，正在重新申请资源...")
                self.event = await manager.allocate(self.resource, priority=self.priority)
                if self.event is None:
                    raise exceptions.AllocateResourceFailed
                logger.info(f"操作[{op.id}]已从挂起恢复")
            elif not silence:
                logger.info(f"操作[{op.id}]正常运行")
            
            return True
        except exceptions.AllocateResourceFailed as e:
            logger.warning(f"操作[{id}]从挂起中恢复时重新申请资源失败: {e}")
            raise e
        except exceptions.ReleaseResourceFailed as e:
            logger.warning(f"操作[{id}]挂起时释放资源失败: {e}")
            raise e
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