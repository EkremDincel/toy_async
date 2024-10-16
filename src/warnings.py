import time
from functools import wraps
from .local import in_async_context


def _wrap_in_warning(obj, name, warning, condition=lambda: True):
	func = getattr(obj, name)

	@wraps(func)
	def wrapper(*args, **kwargs):
		if condition():
			raise Warning(warning)
		else:
			func(*args, **kwargs)

	setattr(obj, name, wrapper)
	setattr(obj, "_noasyncwarning_" + name, func)


def enable_warnings():
	# NOTE: this should be done after the sleep waker imports time.sleep, I think? Or just use _noasyncwarning_sleep?
	_wrap_in_warning(time, "sleep", "Calling time.sleep in an async context.", in_async_context)
