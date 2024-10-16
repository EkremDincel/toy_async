# this is a very crude and one dimensional performance test, but it is better than nothing

from toy_async import Scheduler, gather, sleep
import asyncio
from timeit import default_timer


def toy_async_stress():
	async def nop():
		await sleep(1)
		return 1

	async def main():
		# TODO: make the return type of these a Result and add methods similar to Task (result_or_raise etc) 
		print(sum(map(lambda t: t[0], await gather(nop() for i in range(100000)))))

	s = Scheduler()
	s.mainloop(main())


def asyncio_stress():
	async def nop():
		await asyncio.sleep(1)
		return 1

	async def main():
		print(sum(await asyncio.gather(*(nop() for i in range(100000)))))

	asyncio.run(main())


now = default_timer()
toy_async_stress()
print("toy_async", default_timer() - now)

now = default_timer()
asyncio_stress()
print("asyncio", default_timer() - now)
