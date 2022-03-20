from .waker import AbstractWaker, result

class WakerCondition(AbstractWaker):

	def __init__(self):
		self.waiting = {}

	def __call__(self, ready):
		for condition in self.waiting:
			if condition():
				ready((self.waiting.pop(condition), None))

	def sched(self, function, context, ready):
		self.waiting[context] = function

	def max_sleep(self):
		return 0

	def is_empty(self):
		return not self.waiting