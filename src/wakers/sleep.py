from time import time, sleep as thread_sleep
import heapq
from .waker import AbstractWaker
from ..commands import put_to_sleep

__all__ = ["sleep"]

def sleep(duration):
	return put_to_sleep(WakerSleep, time() + duration)

class WakerSleep(AbstractWaker):
	def __init__(self, awaken):
		self.awaken = awaken
		self.sleeping = []
		self.sleeping_sequence = 0

	def __call__(self):
		while self.sleeping:
			deadline, sequence, task = heapq.heappop(self.sleeping)
			delta = deadline - time()
			if delta > 0:
				heapq.heappush(self.sleeping, (deadline, sequence, task))
				return
			self.awaken((task, None))
		
	def schedule(self, task, context):
		self.sleeping_sequence += 1
		#deadline = time() + context
		heapq.heappush(self.sleeping, (context, self.sleeping_sequence, task))

	def max_sleep(self):
		if self.is_empty():
			return float("inf")
		return self.sleeping[0][0] - time()

	def is_empty(self):
		return not self.sleeping

	def sleep(self, time):
		thread_sleep(time)

	def close(self):
		pass

	def __repr__(self):
		return repr(self.sleeping)