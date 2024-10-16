from toy_async import *


async def second():
	await sleep(2)
	print("Second finished")
	return 2


async def first():
	await sleep(1)
	print("First finished")
	return 1


async def main():
	finished = (await select((first(), second())))[0]
	print(finished.result())


Scheduler().mainloop(main())
