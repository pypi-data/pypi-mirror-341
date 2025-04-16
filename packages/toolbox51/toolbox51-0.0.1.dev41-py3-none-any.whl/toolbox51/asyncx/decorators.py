

import traceback
import functools
import inspect
import uuid
from typing import TypeVar, ParamSpec
from types import NoneType
from collections.abc import Sequence, Callable, Awaitable

from toolbox51 import logger, SingletonMeta

from .manager import manager
from . import exceptions

P = ParamSpec('P')
R = TypeVar('R')



class InvalidFieldPath(metaclass=SingletonMeta):
    ...
IFP = InvalidFieldPath()

class NotGiven(metaclass=SingletonMeta):
    ...
NG = NotGiven()

def get_value_from_field_path(
    func_name: str,
    bound_args: inspect.BoundArguments, 
    key: Sequence[str], valid_types: tuple[type, ...]|None = None,
) -> object:
    key_str = key[0]
    value = bound_args.arguments.get(key[0], IFP)
    if value is IFP:
        raise ValueError(f"{func_name}缺少参数{key_str}")
    for k in key[1:]:
        key_str += f".{k}"
        if isinstance(value, dict):
            value = value.get(k, IFP)
        else:
            value = getattr(value, k, IFP)
        if value is IFP:
            raise ValueError(f"{func_name}缺少参数{key_str}")
    if valid_types is None or isinstance(value, valid_types):
        return value
    raise TypeError(f"{func_name}中的参数{key_str}类型错误，应该为{valid_types}")



def register_op_wrapper_factory(
    func: Callable[P, Awaitable[R]],
    op_id_fp: list[str]|None = None, 
    priority_fp: list[str]|None = None, 
    raise_on_terminate: Exception|None = None, return_on_terminate: R|NotGiven = NG,
) -> Callable[P, Awaitable[R]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("只支持异步函数")
    
    op_id_fp = op_id_fp or ["op_id"]
    priority_fp = priority_fp or ["priority"]
    
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # 获取参数名称
        sig = inspect.signature(func)
        try:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
        except TypeError as e:
            raise TypeError(f"{func.__name__}参数绑定失败: {e}")

        # 获取op_id与priority
        op_id = get_value_from_field_path(func.__name__, bound_args, op_id_fp, (str, uuid.UUID))
        assert isinstance(op_id, (str, uuid.UUID))
        priority = get_value_from_field_path(func.__name__, bound_args, priority_fp, (int, NoneType))
        assert isinstance(priority, (int, NoneType))
        await manager.register(op_id, priority=priority)

        try:
            return await func(*args, **kwargs)
        except exceptions.TerminatedSignal as e:
            if raise_on_terminate is not None:
                raise raise_on_terminate
            if not isinstance(return_on_terminate, NotGiven):
                return return_on_terminate
            raise e
    return wrapper

def register_op(
    op_id_fp: list[str]|None|Callable[P, Awaitable[R]] = None,  # 使用@register_task直接装饰时，op_id_fp为Callable[P, Awaitable[R]]
    priority_fp: list[str]|None = None, 
    raise_on_terminate: Exception|None = None, return_on_terminate: R|NotGiven = NG,
) -> Callable[P, Awaitable[R]] | Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    自动注册操作
    会自动创建新任务，并分配给op
    op_id必须是已注册的op
    如果发现重复注册的task，则不会有任何操作
    """
    
    if callable(op_id_fp):
        # 使用@register_task装饰，此时无法传入其他参数
        func = op_id_fp
        wrapper = register_op_wrapper_factory(func)
        return wrapper
    
    def f(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        wrapper = register_op_wrapper_factory(func, op_id_fp, priority_fp, raise_on_terminate, return_on_terminate)
        return wrapper
    return f



def register_task_wrapper_factory(
    func: Callable[P, Awaitable[R]],
    op_id_fp: list[str]|None = None, 
    raise_on_terminate: Exception|None = None, return_on_terminate: R|NotGiven = NG,
) -> Callable[P, Awaitable[R]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("只支持异步函数")
    
    op_id_fp = op_id_fp or ["op_id"]
    
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # 获取参数名称
        sig = inspect.signature(func)
        try:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
        except TypeError as e:
            raise TypeError(f"{func.__name__}参数绑定失败: {e}")

        # 获取op_id与priority
        op_id = get_value_from_field_path(func.__name__, bound_args, op_id_fp, (str, uuid.UUID))
        assert isinstance(op_id, (str, uuid.UUID))
        await manager.register_task(op_id)
        # await manager.register(op_id, priority=priority)

        try:
            return await func(*args, **kwargs)
        except exceptions.TerminatedSignal as e:
            if raise_on_terminate is not None:
                raise raise_on_terminate
            if not isinstance(return_on_terminate, NotGiven):
                return return_on_terminate
            raise e
    return wrapper

def register_task(
    op_id_fp: list[str]|None|Callable[P, Awaitable[R]] = None,  # 使用@register_task直接装饰时，op_id_fp为Callable[P, Awaitable[R]]
    raise_on_terminate: Exception|None = None, return_on_terminate: R|NotGiven = NG,
) -> Callable[P, Awaitable[R]] | Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    自动注册操作
    会自动创建新任务，并分配给op
    op_id必须是已注册的op
    如果发现重复注册的task，则不会有任何操作
    """
    
    if callable(op_id_fp):
        # 使用@register_task装饰，此时无法传入其他参数
        func = op_id_fp
        wrapper = register_task_wrapper_factory(func)
        return wrapper
    
    def f(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        wrapper = register_task_wrapper_factory(func, op_id_fp, raise_on_terminate, return_on_terminate)
        return wrapper
    return f



def using_resource_wrapper_factory(
    func: Callable[P, Awaitable[R]],
    name_fp: list[str]|None = None,
    url_fp: list[str]|None = None,
    priority_fp: list[str]|None = None,
    validate_fp: list[str]|None = None, parallel_fp: list[str]|None = None,
) -> Callable[P, Awaitable[R]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("只支持异步函数")
    
    name_fp = name_fp or ["name"]
    url_fp = url_fp or ["url"]
    priority_fp = priority_fp or ["priority"]
    validate_fp = validate_fp or ["validate"]
    parallel_fp = parallel_fp or ["parallel"]
    
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # 获取参数名称
        sig = inspect.signature(func)
        try:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
        except TypeError as e:
            raise TypeError(f"{func.__name__}参数绑定失败: {e}")

        # 获取参数
        name = get_value_from_field_path(func.__name__, bound_args, name_fp, (str,))
        assert isinstance(name, str)
        url = get_value_from_field_path(func.__name__, bound_args, url_fp, (str, NoneType))
        assert isinstance(url, (str, NoneType))
        priority = get_value_from_field_path(func.__name__, bound_args, priority_fp, (int, NoneType))
        assert isinstance(priority, (int, NoneType))
        validate = get_value_from_field_path(func.__name__, bound_args, validate_fp, (bool,))
        assert isinstance(validate, bool)
        parallel = get_value_from_field_path(func.__name__, bound_args, parallel_fp, (int, NoneType))
        assert isinstance(parallel, (int, NoneType))
        
        # 检查任务终止
        await manager.check_terminate(logger_stacklevel=3)
        
        # 申请资源
        if url is not None:
            name = f"{name}@{url}"        
        event = await manager.allocate(name, priority=priority)
        if event is None:
            raise exceptions.AllocateResourceFailed(f"Failed to allocate resource {name}.")
        try:
            try:
                await event.wait()
                return await func(*args, **kwargs)
            finally:
                # 释放资源
                await manager.release(name)
        except exceptions.ReleaseResourceFailed as e:
            raise e
        except Exception as e:
            logger.error(f"等待资源或执行任务失败: {e}")
            traceback.print_exc()
            raise e
    return wrapper
    
def using_resource(
    name_fp: list[str]|None|Callable[P, Awaitable[R]] = None,
    url_fp: list[str]|None = None,
    priority_fp: list[str]|None = None,
    validate_fp: list[str]|None = None, parallel_fp: list[str]|None = None,
) -> Callable[P, Awaitable[R]] | Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    自动申请/释放资源
    """
    if callable(name_fp):
        # 使用@using_resource装饰，此时无法传入其他参数
        func = name_fp
        wrapper = using_resource_wrapper_factory(func)
        return wrapper
    
    def f(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        wrapper = using_resource_wrapper_factory(func, name_fp, url_fp, priority_fp, validate_fp, parallel_fp)
        return wrapper
    return f



def using_resource_static(
    resource: str,
    *, 
    url: str|None = None,
    priority: int|None = None,
    validate: bool = False, parallel: int|None = None, 
):
    if url is not None:
        resource = f"{resource}@{url}"
    if validate and not manager.touch_resource(resource, parallel=parallel):
        raise exceptions.InvalidResource(f"Invalid resource: {resource}")
    
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        if not callable(func) or not func.__code__.co_flags & 0x0080:
            raise TypeError(f"Decorator {using_resource.__name__} can only be used on async functions")
        
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            await manager.check_terminate(logger_stacklevel=3)
            event = await manager.allocate(resource, priority=priority)
            if event is None:
                raise exceptions.AllocateResourceFailed(f"Failed to allocate resource {resource}.")
            try:
                try:
                    await event.wait()
                    return await func(*args, **kwargs)
                finally:
                    await manager.release(resource)
            except exceptions.ReleaseResourceFailed as e:
                raise e
            except Exception as e:
                logger.error(f"等待资源或执行任务失败: {e}")
                traceback.print_exc()
                raise e
        return wrapper
    return decorator