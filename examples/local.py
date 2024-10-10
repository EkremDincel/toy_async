from toy_async import *


async def hello():
	print("Hello World")


async def main():
	get_running_scheduler().create_task(hello())
	assert get_running_scheduler() == get_current_scheduler()


get_current_scheduler().mainloop(main())

try:
	get_running_scheduler()
except ValueError:
	pass
else:
	assert False, "There shouldn't be an active scheduler."
