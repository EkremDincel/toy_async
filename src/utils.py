from .commands import get_scheduler

async def run(coroutine):
	s = await get_scheduler
	return s.create_task(coroutine)

async def run_all(coroutines):
	s = await get_scheduler
	return s.create_tasks(coroutines)