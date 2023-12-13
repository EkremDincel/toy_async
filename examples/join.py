from toy_async import *

async def hi():
	print("Hello")
	return 1

async def goodbye():
	await sleep(1)
	print("Goodbye")
	return 2

async def main():
	tasks = await run_all([hi(), goodbye()])
	results = list(await join(tasks))
	print(results)
	print("End")

s = Scheduler()
s.mainloop(main())