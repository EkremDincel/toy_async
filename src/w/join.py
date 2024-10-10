from .waker import AbstractWaker, result
import inspect


class WakerJoin(AbstractWaker):
	def __init__(self):
		self.joined = {}

	def __call__(self, ready):
		ready_functions = []

		for joined_on in self.joined:
			if all(inspect.getcoroutinestate(c) == inspect.CORO_CLOSED for c in joined_on):
				ready_functions.append(joined_on)

		for i in ready_functions:
			# how to return the value instead of `None`?
			ready((self.joined.pop(i), None))

	def sched(self, function, context, ready):
		self.joined[context] = function
		for joined_on in context:
			ready((joined_on, None))

	# bunun çöz
	def max_sleep(self):
		return float("inf")

	def is_empty(self):
		return not self.joined


def join(*coroutines):
	return result(WakerJoin, coroutines)
