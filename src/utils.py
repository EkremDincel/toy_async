from .wakers.waker import result
import inspect

# can we replace this with a trivial waker?
class Awaitable:
    def __await__(self):
        return (yield)

switch = Awaitable

def run(coroutine):
    return result(None, coroutine)

class WaitFor():

    def __init__(self, coroutine):
        self.coroutine = coroutine

    def __await__(self):
        # just use a Task wrapper, duh! 
        while inspect.getcoroutinestate(self.coroutine) != inspect.CORO_CLOSED:
            yield
        return

async def join(*coroutines):
    for i in coroutines:
        await run(i)
    for i in coroutines:
        await WaitFor(i)