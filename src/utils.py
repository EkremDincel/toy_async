from .commands import get_scheduler

async def run(coroutine):
	s = await get_scheduler
	return s.create_task(coroutine)

async def run_all(coroutines):
	s = await get_scheduler
	return s.create_tasks(coroutines)

async def as_completed(coroutines): # return an async iter
	pass

async def select(coroutines, n=1): # select the first completed
	pass