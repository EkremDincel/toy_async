from .scheduler import Scheduler


def block_on(coroutine):
	return Scheduler().mainloop(coroutine)
