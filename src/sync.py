from .scheduler import Scheduler
from .task import Task


def block_on(coroutine):
	Scheduler().mainloop(Task(coroutine))
	return task.result
