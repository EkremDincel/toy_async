from toy_async import *


async def hi():
	print("Hello")
	return 1


async def goodbye():
	await sleep(1)
	print("Goodbye")
	raise ValueError()


async def main():
	tasks = run_all([hi(), goodbye()])
	for result, exception in await join(tasks):
		if exception is None:
			print("Return:", repr(result))
		else:
			print("Exception:", repr(exception))
	print("End")


s = Scheduler(debug=False)
s.mainloop(main())
