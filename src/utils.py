# can we replace this with a trivial waker?
class Awaitable:
    def __await__(self):
        return (yield)

switch = Awaitable