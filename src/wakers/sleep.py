from ..timer import timer, thread_sleep
import heapq
from .waker import AbstractWaker
from ..commands import put_to_sleep

__all__ = ["sleep"]


def sleep(duration):
	return put_to_sleep(WakerSleep, timer() + duration)


class WakerSleep(AbstractWaker):
	def __init__(self, awaken):
		self.awaken = awaken
		self.sleeping = []
		self.removed = set()
		self.sleeping_sequence = 0

	def __call__(self):
		current_time = timer()
		while self.sleeping:
			deadline, sequence, task = heapq.heappop(self.sleeping)
			delta = deadline - current_time
			if delta > 0:
				heapq.heappush(self.sleeping, (deadline, sequence, task))
				return
			self.awaken((task, None))

	def schedule(self, task, deadline):
		self.sleeping_sequence += 1
		# deadline = timer() + context # we are doing this in the sleep call
		heapq.heappush(self.sleeping, (deadline, self.sleeping_sequence, task))

	def unschedule(self, task):
		self.removed.add(task)

	def max_sleep(self):
		while self.sleeping:
			deadline, _seq, task = self.sleeping[0]
			if task in self.removed: # if the task is canceled, just pass it
				self.removed.remove(task)
				heapq.heappop(self.sleeping)
			else:
				return deadline - timer()

		return float("inf")

	def is_empty(self):
		return not self.sleeping

	# todo: look into https://stackoverflow.com/a/43505033
	def sleep(self, sleep_time):
		leeway = 1 / 100

		if sleep_time - leeway > leeway:
			before = timer()
			thread_sleep(sleep_time - leeway)

			start = timer()
			spin_time = sleep_time - (start - before)
		else:
			start = timer()
			spin_time = sleep_time

		while (timer() - start) < spin_time:
			pass

	def close(self):
		for task in self.sleeping:
			task.close()

	def __repr__(self):
		return repr(self.sleeping)
