from toy_async import *


async def display(x):
	for i in range(x - 5, x):
		await sleep(1)
		print(i)


s = Scheduler()
s.create_task(display(5))
s.create_task(display(10))
s.run_until_completion()
s.close()