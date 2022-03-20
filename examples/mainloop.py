import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src import *

async def hi():
	print("Hello")
	await sleep(1)
	print("What is your name?")
	return 1

async def goodbye():
	print("Goodbye")
	await sleep(1)
	print("Are you still there?")
	return 2

async def main():
	print(await hi())
	print(await goodbye())

s = Scheduler()
s.mainloop(main())