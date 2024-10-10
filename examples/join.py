from toy_async import *


async def hi():
	print("Hello")
	return 1


async def goodbye():
	await sleep(1)
	print("Goodbye")
	return 2


async def main():
	tasks = run_all([hi(), goodbye()])
	for result in await join(tasks):
		print(result)
	print("End")


s = Scheduler(debug=True)
s.mainloop(main())
