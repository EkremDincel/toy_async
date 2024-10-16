from timeit import default_timer as _timer

try:
	from time import _noasyncwarning_sleep as thread_sleep  # if warnings.py wrapped the sleep function
except ImportError:
	from time import sleep as thread_sleep  # noqa: F401


_monotonic = _timer()


def timer():
	global _monotonic
	current_time = _timer()
	if current_time > _monotonic:
		_monotonic = current_time
	return _monotonic


class Instant:
	def __init__(self):
		self.time = timer()

	def interval(self):
		return timer() - self.time

	def __repr__(self):
		return f"Instant({self.time})"


def now():
	return Instant()
