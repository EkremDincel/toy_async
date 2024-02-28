from threading import local
from functools import wraps

_local = local()
_local.current = None
_local.running = None

__all__ = ["set_current_scheduler", "set_default_scheduler", "get_current_scheduler", "get_running_scheduler"]

def set_current_scheduler(scheduler):
	_local.current = scheduler

def set_default_scheduler(scheduler):
	if _local.current is None:
		set_current_scheduler(scheduler)
	return _local.current

def get_current_scheduler(*args, **kwargs):
	if _local.current is None:
		# this is imported here to prevent a import cycle
		from .scheduler import Scheduler
		set_current_scheduler(Scheduler(*args, **kwargs))

	return _local.current

def get_running_scheduler():
	if _local.running is None:
		raise ValueError("No running scheduler")
	return _local.running

def _running_guard(f):
	@wraps(f)
	def set_running(self, *args, **kwargs):
		_local.running = self
		try:
			f(self, *args, **kwargs)
		except BaseException as e:
			raise e
		finally:
			_local.running = None

	return set_running