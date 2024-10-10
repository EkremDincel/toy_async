import abc
from collections import namedtuple


class AbstractWaker(abc.ABC):
	@abc.abstractmethod
	def __init__(self, awaken):
		pass

	@abc.abstractmethod
	def __call__(self):
		pass

	@abc.abstractmethod
	def schedule(self, task, context):
		pass

	@abc.abstractmethod
	def max_sleep(self):
		pass

	@abc.abstractmethod
	def is_empty(self):
		pass
