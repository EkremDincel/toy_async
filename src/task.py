from abc import ABC, abstractmethod
from .commands import switch
from .timer import now

# see for atomics https://stackoverflow.com/a/27062830


class CancelledError(GeneratorExit):  # Question: GeneratorExit is raised in coroutine.close anyway. Is cancel method necessary?
	pass


class TaskNotFinishedError(RuntimeError):
	pass


class AbstractTask:
	@abstractmethod
	def _set_result(self, result):
		raise NotImplementedError()

	@abstractmethod
	def _set_error(self, error):
		raise NotImplementedError()

	@abstractmethod
	def send(self, arg):
		raise NotImplementedError()

	@abstractmethod
	def finished(self):
		raise NotImplementedError()

	@abstractmethod
	def error(self):
		raise NotImplementedError()

	@abstractmethod
	def result(self):
		raise NotImplementedError()

	@abstractmethod
	def result_or_raise(self):
		raise NotImplementedError()

	@abstractmethod
	async def wait(self, timeout):
		raise NotImplementedError()

	@abstractmethod
	def throw(self, error):
		raise NotImplementedError()

	@abstractmethod
	def cancel(self, *args, **kwargs):
		raise NotImplementedError()

	@abstractmethod
	def close(self):
		raise NotImplementedError()

	def name(self):
		raise NotImplementedError()

	def set_name(self):
		raise NotImplementedError()


class Task(AbstractTask):
	def __init__(self, coroutine):
		self._waker = None  # todo: try using this for JoinWaker or task.wait
		self._coroutine = coroutine
		self._finished = False
		self._result = None
		self._exception = None
		self._name = coroutine.__name__

	def send(self, arg):
		return self._coroutine.send(arg)

	def _set_result(self, result):
		self._finished = True
		self._result = result

	def _set_error(self, error):
		self._finished = True
		self._exception = error

	def finished(self):
		return self._finished

	async def wait(self, timeout=float("inf")):
		start = now()
		while not self._finished and timeout > start.interval():
			await switch
		return self._result

	def throw(self, error):
		return self._coroutine.throw(error)

	def cancel(self, *args, **kwargs):
		return self.throw(CancelledError(*args, **kwargs))

	def error(self):
		if self._finished:
			return self._exception
		raise TaskNotFinishedError(self)

	def result(self):
		if self._finished:
			return self._result
		raise TaskNotFinishedError(self)

	def result_or_raise(self):
		if self._finished:
			if self._exception is not None:
				raise self._exception
			return self._result
		raise TaskNotFinishedError(self)

	def close(self):
		return self._coroutine.close()

	def name(self):
		return self._name

	def set_name(self, name):
		self._name = name


class ThreadTask(Task):
	pass


class CallbackTask(Task):
	pass


class ChildTask(Task):
	pass


class ShieldTask(Task):
	pass
