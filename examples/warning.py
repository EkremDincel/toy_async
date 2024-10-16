from toy_async import enable_warnings, Scheduler, sleep, AbortTaskError

enable_warnings()  # enable all warnings *before* importing any other module

from time import sleep as thread_sleep
import traceback
import sys


async def wrong_sleep():
	try:
		thread_sleep(1)
	except Warning as e:
		traceback.print_exc(file=sys.stdout)
		raise AbortTaskError(e)
	else:
		raise RuntimeError("Can't observe the warning.")
	finally:
		print("Called wrong_sleep")


async def right_sleep():
	await sleep(1)
	print("Called right_sleep")


s = Scheduler()
s.create_tasks([right_sleep(), wrong_sleep()])
s.run_until_completion()
s.close()
