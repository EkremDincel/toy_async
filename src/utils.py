from .local import get_running_scheduler
from .wakers.sleep import sleep
from .wakers.join import join
from .commands import switch


def run(coroutine):
	s = get_running_scheduler()
	return s.create_task(coroutine)


def run_all(coroutines):
	s = get_running_scheduler()
	return s.create_tasks(coroutines)


async def gather(coroutines):
	tasks = run_all(coroutines)
	return await join(tasks)


def as_completed(coroutines):  # return an async iter
	pass


# TODO: create a waker for this
async def select(coroutines, n=1):  # select the first completed
	tasks = set(run_all(coroutines))
	selected = []
	while len(selected) < n:
		await switch
		to_remove = []
		for task in tasks:
			if task.finished():
				selected.append(task)
				to_remove.append(task)
		for task in to_remove:
			tasks.remove(task)

	for task in tasks:
		task.cancel()

	return selected


def call_soon(function):
	async def inner():
		return function()

	return run(inner())


def call_later(function, delay):
	async def inner():
		await sleep(delay)
		return function()

	return run(inner())


# def async unconstrained():
# 	pass
