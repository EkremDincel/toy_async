from abc import ABC, abstractmethod
from .commands import switch
from .timer import now
from .local import get_running_scheduler

# see for atomics https://stackoverflow.com/a/27062830


class TaskCancelledError(
	GeneratorExit
):  # Question: GeneratorExit is raised in coroutine.close anyway. Is cancel method necessary?
	pass


class AbortTaskError(GeneratorExit):
	pass


class TaskNotFinishedError(RuntimeError):
	pass


class AbstractTask(ABC):
	@abstractmethod
	def _set_result(self, result):
		raise NotImplementedError()

	@abstractmethod
	def _set_error(self, error):
		raise NotImplementedError()

	@abstractmethod
	def _result_error_tuple(self):
		raise NotImplementedError()

	@abstractmethod
	def _resume(self, arg):
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
	def _throw(self, error):
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
	_cancelled = False

	def __init__(self, coroutine):
		self._waker = None  # todo: try using this for JoinWaker or task.wait
		self._coroutine = coroutine
		self._finished = False
		self._result = None # I don't know how good of an idea this is
		self._exception = None # note: None cannot be used with raise, so this means no exception
		self._name = coroutine.__name__

	def _resume(self, arg):
		return self._coroutine.send(arg)

	def _set_result(self, result):
		self._finished = True
		self._result = result

	def _set_error(self, error):
		self._finished = True
		self._exception = error

	def _result_error_tuple(self):
		return (self._result, self._exception)

	def finished(self):
		return self._finished

	async def wait(self, timeout=float("inf")):
		start = now()
		while not self._finished and timeout > start.interval():
			await switch
		return self.result_or_raise()

	def _throw(self, error):
			return self._coroutine.throw(error)

	def cancel(self, *args, **kwargs): # NOTE: the task might step once more before the cancelation
		if self._waker is not None:
			self._waker.unschedule(self)
		if self._cancelled:
			return
		self._cancelled = True
		get_running_scheduler()._awaken((self, None, TaskCancelledError(*args, **kwargs)))

	def cancelled():
		return self._cancelled

	def error(self):
		if self._finished:
			if self._exception is None:
				raise ValueError("The task has not terminated with an exception. It terminated with a return value.")
			return self._exception
		raise TaskNotFinishedError(self)

	def result(self):
		if self._finished:
			if self._exception is not None:
				raise ValueError("The task has not terminated with a return value. It terminated with an exception.")
			return self._result
		raise TaskNotFinishedError(self)

	def result_or_raise(self):
		if self._finished:
			if self._exception is not None:
				raise self._exception
			return self._result
		raise TaskNotFinishedError(self)

	def close(self): # Question: should this be public?
		return self._coroutine.close()

	def name(self):
		return self._name

	def set_name(self, name):
		self._name = name

	def __repr__(self):
		return f"Task({self._name!r})"


class ThreadTask(Task):
	pass


class CallbackTask(Task):
	pass


class ChildTask(Task):
	pass


class ShieldableTask(Task):
	pass
