from toy_async import *
from functools import wraps, partial

class Repeater:
	def __init__(self):
		self.scheduler = Scheduler()

	def repeat(self, function, interval, *, delay = 0, count = float('inf')):
		@wraps(function)
		async def waiter():
			await sleep(delay)
			if count <= 0:
				return

			current = 0
			while True:
				result = function()
				if result is not None and result == False:
					break

				current += 1
				if not current < count:
					break
				await sleep(interval)

		self.scheduler.create_task(waiter())

	def run(self):
		self.scheduler.run_until_completion()


r = Repeater()
r.repeat(partial(print, "Hello", end = "", flush = True), 1, count = 5)
r.repeat(partial(print, " World!"), 1, delay = 0.5, count = 5)
r.run()