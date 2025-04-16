

# Op and Task

class TerminatedSignal(Exception):
    """Op结束信号"""
    pass

class UnregisteredOperation(Exception):
    """未注册的Op"""
    pass

class DuplicatedOperationID(Exception):
    """注册Op时使用了重复的ID"""
    pass

class UnregisteredTask(Exception):
    """未注册的Task"""
    pass

class InvalidTask(Exception):
    """无法获得当前Task（不在协程内或其他原因，导致asyncio不报错但回复None）"""
    pass



# Resource

class InvalidResource(Exception):
    """无效的资源"""
    pass

class DuplicatedResource(Exception):
    """重复注册资源，且参数不一致"""
    pass

class AllocateResourceFailed(Exception):
    """分配资源失败"""
    pass

class ReleaseResourceFailed(Exception):
    """释放资源失败"""
    pass