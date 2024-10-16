from toy_async import *


async def foo(x):
	try:
		await sleep(1)
	except ValueError:
		print("Error")
	else:
		print(x)


async def multiple_tasks():
	task = run(foo("Hello"))
	await sleep(0.5)
	print("Canceling")
	task.throw(ValueError)
	print("Cancelled")


# s = Scheduler(debug=True)
# s.mainloop(multiple_tasks())
