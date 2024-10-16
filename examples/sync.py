from toy_async import *


async def red_function():
	print("Red")
	await sleep(1)
	return "Blue"


result = block_on(red_function())
print(result)
