import abc

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

	# @abc.abstractmethod
	# def max_sleep_for_task(self): # task.waker.max_sleep_for_task(task) should be the used
	# 	pass

	@abc.abstractmethod
	def is_empty(self):
		pass

	@abc.abstractmethod
	def sleep(self):
		pass

	@abc.abstractmethod
	def close(self):
		pass