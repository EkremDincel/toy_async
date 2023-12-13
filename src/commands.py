from .result import result, Command

__all__ = ["get_scheduler", "switch", "put_to_sleep"]

get_scheduler = result(Command.GET)
switch = result(Command.SWITCH)
def put_to_sleep(waker, context = None):
	return result(Command.PUT_TO_SLEEP, context, waker)