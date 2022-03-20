from collections import deque
from time import sleep as thread_sleep
import abc

class Scheduler():
	def __init__(self):
		self.ready = deque()
		self.wakers = {}

	def sched(self, function, waker_type, context):
		self.wakers.setdefault(waker_type, waker_type())
		waker = self.wakers[waker_type]
		context = waker.sched(function, context, self.ready.append)

	def call_soon(self, function):
		self.ready.append((function, None))

	def run(self):
		def step_coroutine(function, value):
			try:
				result = function.send(value)
			except StopIteration as e:
				#function.value = e.value
				pass
			else:
				if result is None: # just suspend
					self.ready.append((function, None))
				elif result.waker is None: # this is not a checkpoint
					self.ready.append((result.context, None))
					step_coroutine(function, None) # continue immediately
				else: # a checkpoint
					self.sched(function, result.waker, result.context)

		while True:
			lenght = len(self.ready)
			if lenght == 0:
				if all(i.is_empty() for i in self.wakers.values()):
					break
				else:
					# we should use a better algo and also exploit the timeout arg of `select` for WakerIO
					sleep_duration = min([i.max_sleep(), float("inf")][i.is_empty()] for i in self.wakers.values())
					if sleep_duration > 0:
						thread_sleep(sleep_duration)


			for _ in range(lenght):
				function, value = self.ready.popleft()
				step_coroutine(function, value)

			for waker in self.wakers.values():
				waker(self.ready.append)

	def mainloop(self, function):
		self.call_soon(function)
		self.run()

PROTO_CONTINUE = None
PROTO_SLEEP = 0
PROTO_APPEND = 1