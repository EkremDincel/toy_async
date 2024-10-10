from toy_async import *

async def delayed():
	for i in range(1, 4):
		call_delayed(lambda i=i: print(i), i)
	print(0)


async def instant():
	for i in range(1, 4):
		call_later(lambda i=i: print(i))
	print(0)


async def main():
	await instant()
	await switch
	print()
	await delayed()

s = Scheduler()
s.mainloop(main())
