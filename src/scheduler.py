from collections import deque
from .result import Command
from .task import Task
from time import time
from .local import set_default_scheduler, _running_guard

__all__ = ["Scheduler"]

class Scheduler():
	def __init__(self, debug = False):
		self.awake = deque()
		self.wakers = {}

		set_default_scheduler(self)

		# debug
		self.debug = debug
		self.step_count = 0
		self.total_sleep = 0
		self.start = None

	def log(self, *args, **kwargs):
		if self.debug:
			print(*args, **kwargs)

	def put_to_sleep(self, task, waker_type, context):
		try:
			waker = self.wakers[waker_type]
		# since this will be a cold path we are using try except instead of set_default
		except KeyError:
			waker = self.wakers[waker_type] = waker_type(self.awake.append)

		waker.schedule(task, context)

	def spawn_task(self, task):
		assert isinstance(task, Task), "didn't suplied a task"
		self.awake.append((task, None))

	def spawn_tasks(self, tasks):
		assert all(map(lambda x: isinstance(x, Task), tasks)), "didn't suplied a task"
		self.awake.extend((task, None) for task in tasks)

	def create_task(self, coroutine):
		task = Task(coroutine)
		self.spawn_task(task)
		return task

	def create_tasks(self, coroutines):
		tasks = tuple(map(Task, coroutines))
		self.spawn_tasks(tasks)
		return tasks

	# Question: is this a good place for this?
	@_running_guard
	def step_task(self, task, value, err = None):
		self.step_count += 1
		if err is not None:
			task.throw(err)

		try:
			result = task.coroutine.send(value)
		except StopIteration as e:
			task.set(e.value)
		else:
			if result.command == Command.PUT_TO_SLEEP:
				self.put_to_sleep(task, result.waker, result.context)
			elif result.command == Command.SWITCH:
				self.awake.append((task, None))
			elif result.command == Command.GET:
				self.step_task(task, self)
			else:
				raise ValueError("Invalid Command", result.command)

	def run_once(self):
		for waker in self.wakers.values():
			waker()

		lenght = len(self.awake)
		for _ in range(lenght):
			task, context = self.awake.popleft()
			self.step_task(task, context)

	def wait(self):
		lenght = len(self.awake)

		if lenght == 0:
			if all(waker.is_empty() for waker in self.wakers.values()):
				# there is no task left, neither awake nor asleep
				return True
			else:
				# io wakers simply need to return 0 for max_sleep and they will be used for sleeping
				non_empty_wakers = filter(lambda x: not x.is_empty(), self.wakers.values())
				waker, sleep_duration = min(((waker, waker.max_sleep()) for waker in non_empty_wakers), key = lambda x: x[1])
				self.log(sleep_duration)
				#self.log(self.awake)
				self.total_sleep += sleep_duration
				waker.sleep(sleep_duration)
		return False

	def clear_wakers(self):
		for waker in self.wakers.values():
			# might use a way to keep track how long the waker stays unused here
			# also we might want to have a list of permanent wakers
			if waker.is_empty():
				wakers.pop(type(waker))

	def run_until_completion(self):
		self.start = time()
		while True:
			stop = self.wait()
			if stop:
				break
			self.run_once()
		self.log("total steps:", self.step_count)
		dilation = time() - self.start
		self.log("total uptime (seconds): {:.6f}/{:.6f}".format(dilation - self.total_sleep, dilation))

	def close(self):
		for waker in self.wakers.values():
			waker.close()

	def mainloop(self, coroutine):
		self.create_task(coroutine)
		self.run_until_completion()
		self.close()
		
	# TODO: how should this work? wrap it in a task and return perhaps? should it be a coroutine or function?
	def to_thread(self, coroutine):
		pass