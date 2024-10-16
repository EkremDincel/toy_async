from toy_async import *


async def foo(x):
	try:
		await sleep(1) # the error is caused by the waker waking this after it is canceled
	except TaskCancelledError:
		print("Cancel detected in foo")
	else:
		print(x)


async def multiple_tasks():
	task = run(foo("Hello"))
	await sleep(0.5)
	print("Canceling foo")
	task.cancel()
	await task.wait()
	print("Cancelled foo")


s = Scheduler(debug=False)
s.mainloop(multiple_tasks())

