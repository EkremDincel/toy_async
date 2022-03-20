import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src import *

async def display(x):
	for i in range(x-5, x):
		await sleep(1)
		print(i)

s = Scheduler()
s.call_soon(display(5))
s.call_soon(display(10))
s.run()