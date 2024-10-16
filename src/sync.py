from .scheduler import Scheduler


def block_on(coroutine):
	return Scheduler().mainloop(coroutine)  # Question: would this create problems if use it in a already running Scheduler?
