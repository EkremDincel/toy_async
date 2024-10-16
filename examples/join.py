from toy_async import *


async def hi():
	print("Hello")
	return 1


async def goodbye():
	await sleep(1)
	print("Goodbye")
	raise ValueError("Error")


async def main():
	tasks = run_all([hi(), goodbye()])
	for task, (result, exception) in zip(tasks, await join(tasks)):
		if exception is None:
			print(f"[{task.name()}] return:", repr(result))
		else:
			print(f"[{task.name()}] exception:", repr(exception))
	print("End")


s = Scheduler(debug=False)
s.mainloop(main())
