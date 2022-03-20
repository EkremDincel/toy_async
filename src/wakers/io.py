from .waker import AbstractWaker, result
from select import select

(CTX_READ,
CTX_WRITE,
) = range(2)

class WakerIO(AbstractWaker):
	
	def __init__(self):
		self.read_waiting = {}
		self.write_waiting = {}

	def __call__(self, ready):
		can_read, can_write, _ = select(self.read_waiting, self.write_waiting, [], 0)

		for fd in can_read:
			ready((self.read_waiting.pop(fd), None))
		for fd in can_write:
			ready((self.write_waiting.pop(fd), None))

	def sched(self, function, context, ready):
		fileno, ctx = context
		if ctx == CTX_READ:
			self.read_waiting[fileno] = function
		else:
			self.write_waiting[fileno] = function
		
	def max_sleep(self):
		return 0

	def is_empty(self):
		return not self.read_waiting and not self.write_waiting


def wait_read(fileno):
	return result(WakerIO, (fileno, CTX_READ))

def wait_write(fileno):
	return result(WakerIO, (fileno, CTX_WRITE))