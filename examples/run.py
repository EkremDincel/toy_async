from toy_async import *

async def foo(x):
	await sleep(1)
	print(x)
	return x

async def multiple_tasks():
		t1 = await run(foo("a"))
		t2 = await run(foo("b"))
		await sleep(2)
		print(t1.result, t2.result)

s = Scheduler()
s.mainloop(multiple_tasks())