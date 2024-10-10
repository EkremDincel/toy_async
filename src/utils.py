from .commands import get_scheduler
from .wakers import sleep
from .local import get_running_scheduler
from functools import partial

def run(coroutine):
	s = get_running_scheduler()
	return s.create_task(coroutine)

def run_all(coroutines):
	s = get_running_scheduler()
	return s.create_tasks(coroutines)

def as_completed(coroutines): # return an async iter
	pass

def select(coroutines, n=1): # select the first completed
	pass

def call_later(function):
	async def inner():
		return function()
	return run(inner())

def call_delayed(function, delay):
	async def inner():
		await sleep(delay)
		return function()
	return run(inner())