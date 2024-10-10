from abc import ABC, abstractmethod
from .commands import switch

class AbstractTask:
	@abstractmethod
	def _set(self, result):
		raise NotImplementedError()

	@abstractmethod
	def _get_coroutine(self):
		raise NotImplementedError()

	@abstractmethod
	def finished(self):
		raise NotImplementedError()

	# @abstractmethod
	# def cancel(self):
	# 	raise NotImplementedError()

	@abstractmethod
	def throw(self, error):
		raise NotImplementedError()

	@abstractmethod
	def result(self, timeout):
		raise NotImplementedError()

	# @abstractmethod
	# async def wait(self, timeout):
	# 	raise NotImplementedError()


class Task(AbstractTask):
	def __init__(self, coroutine):
		self._waker = None # todo: try using this for JoinWaker or task.wait
		self._coroutine = coroutine
		self._finished = False
		self._result = None

	def _get_coroutine(self):
		return self._coroutine

	def _set(self, result):
		self._finished = True
		self._result = result

	def finished(self):
		return self._finished

	async def wait(self):
		while not self._finished:
			await switch
		return self._result

	async def throw(self, error):
		return self._coroutine.throw(error)

	def result(self):
		return self._result # Question: should we raise if we didnt finish?