from toy_async import local

async def hello():
	print("Hello World")

async def main():
	local.get_running_scheduler().create_task(hello())
	assert local.get_running_scheduler() == local.get_current_scheduler()

local.get_current_scheduler().mainloop(main())

try:
	local.get_running_scheduler()
except ValueError:
	pass
else:
	assert False, "There shouldn't be an active scheduler."