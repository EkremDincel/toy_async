from toy_async import *


async def hi():
	print("Hello")
	await sleep(1)
	print("How are you?")
	return 1


async def goodbye():
	print("Goodbye")
	await sleep(1)
	print("Are you still there?")
	return 2


async def main():
	print(await hi())
	print(await goodbye())
	return 3


s = Scheduler()
assert s.mainloop(main()) == 3, "Wrong return value."
