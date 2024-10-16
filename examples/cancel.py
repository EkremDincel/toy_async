from toy_async import *


async def foo(x):
	try:
		await sleep(1)
	except BaseException as e:
		print("Throw detected in foo:", repr(e))
		raise e
	else:
		print(x)


async def multiple_tasks():
	task = run(foo("Hello"))
	# await sleep(0.5)
	print("Canceling foo")
	task.cancel()
	print("Cancelled foo")
	try:
		result = await task.wait()
	except BaseException as e:
		print("foo terminated with an exception:", repr(e))
	else:
		print("foo terminated with a return value:", repr(result))


s = Scheduler(debug=False)
s.mainloop(multiple_tasks())
