from toy_async import call_later, call_soon, switch, Scheduler


async def delayed():
	for i in range(1, 4):
		call_later(lambda i=i: print(i), i)
	print(0)


async def instant():
	for i in range(1, 4):
		call_soon(lambda i=i: print(i))
	print(0)


async def main():
	await instant()
	await switch
	print()
	await delayed()


s = Scheduler()
s.mainloop(main())
