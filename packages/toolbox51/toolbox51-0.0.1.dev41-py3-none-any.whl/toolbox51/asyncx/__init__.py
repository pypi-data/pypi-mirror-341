# ruff: noqa



from .exceptions import (
    TerminatedSignal,
    
    UnregisteredOperation, DuplicatedOperationID,
    UnregisteredTask, InvalidTask,
    
    InvalidResource, DuplicatedResource,
    AllocateResourceFailed, ReleaseResourceFailed,
)
from .manager import manager as _manager
from .context_managers import async_closing, AllocateResource
from .context_managers import async_closing, AllocateResource
from .decorators import using_resource



set_default_priority = _manager.set_default_priority
set_default_priority = _manager.set_default_priority

# 任务管理
register = _manager.register
register_task = _manager.register_task
wrap_generator = _manager.wrap_generator
create_task = _manager.create_task
clear_finished_ops = _manager.clear_finished_ops

# 外部操作
terminate = _manager.terminate
kill = _manager.kill
suspend = _manager.suspend
resume = _manager.resume

# 状态检查
check_terminate = _manager.check_terminate

# 资源管理
touch_resource = _manager.touch_resource
register_resource = _manager.register_resource
# allocate = _manager.allocate
# release = _manager.release
