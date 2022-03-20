import abc
from collections import namedtuple

class AbstractWaker(abc.ABC):
	@abc.abstractmethod
	def __init__(self):
		pass

	@abc.abstractmethod
	def __call__(self, ready):
		pass

	@abc.abstractmethod
	def sched(self, function, context, ready):
		pass

	@abc.abstractmethod
	def max_sleep(self):
		pass

	@abc.abstractmethod
	def is_empty(self):
		pass

#result = namedtuple("Result", ("waker", "context"))

class result():

	def __init__(self, waker, context):
		self.waker = waker
		self.context = context

	def __await__(self):
		return (yield self)

def context_with_waker(waker):
	def inner(context):
		return result(waker, context)
	return inner