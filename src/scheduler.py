from collections import deque
from .result import Command
from .task import Task, AbstractTask
from .timer import now
from .local import set_default_scheduler, _running_guard

__all__ = ["Scheduler"]


class Scheduler:
	def __init__(self, debug=False):
		self.awake = deque()
		self.wakers = {}

		set_default_scheduler(self)

		self.closed = False

		# debug
		self.debug = debug
		self.step_count = 0
		self.total_sleep = 0
		self.total_wait_calls = 0
		self.start = None

	def log(self, *args, **kwargs):
		if self.debug:
			print("INFO:\t", *args, **kwargs)

	def _awaken(self, arg):
		task = arg[0]
		task._waker = None
		# if not task.finished(): # !!! NOTE: wakers might try awakening canceled tasks
		# 	# print("Awakening", task.finished()) # ??? Question: why is this false
		# 	self.awake.append(arg)
		self.awake.append(arg)

	def put_to_sleep(self, task, waker_type, context):  # Todo: make private?
		try:
			waker = self.wakers[waker_type]
		# since this will be a cold path we are using try except instead of setdefault
		except KeyError:
			waker = self.wakers[waker_type] = waker_type(self._awaken)

		task._waker = waker
		# self.log(f"set waker of {task} to {type(waker)}")
		waker.schedule(task, context)

	def spawn_task(self, task):
		assert isinstance(task, AbstractTask), "didn't suplied a task"
		self.awake.append((task, None))

	def spawn_tasks(self, tasks):
		assert all(map(lambda x: isinstance(x, AbstractTask), tasks)), "didn't suplied a task"
		self.awake.extend((task, None) for task in tasks)

	def create_task(self, coroutine, task_type=Task):
		task = task_type(coroutine)
		self.spawn_task(task)
		return task

	def create_tasks(self, coroutines, task_type=Task):
		tasks = tuple(map(task_type, coroutines))
		self.spawn_tasks(tasks)
		return tasks

	def _step_task(self, task, value, err=None):
		self.step_count += 1

		try:
			if err is not None:
				self.log("Throwing into:", task.name())
				result = task._throw(err)
			else:
				self.log("Sending to:", task.name())
				result = task._resume(value)
		except StopIteration as e:
			task._set_result(e.value)
		except BaseException as e:  # WARNING: this can quietly discard the errors caused by the runtime
			task._set_error(e)
			if err is not None and task._waker is not None:
				task._waker.unschedule(task)
		else:
			if result.command == Command.PUT_TO_SLEEP:
				self.put_to_sleep(task, result.waker, result.context)
			elif result.command == Command.SWITCH:
				self.awake.append((task, None))
			elif result.command == Command.GET:
				self._step_task(task, self)
			else:
				raise ValueError("Invalid Command", result.command)

	@_running_guard  # Question: is this a good place for this?
	def run_once(self):
		for waker in self.wakers.values():
			waker()

		lenght = len(self.awake)
		for _ in range(lenght):
			task, *context = self.awake.popleft()  # context might include error
			self._step_task(task, *context)

	def wait(self):
		lenght = len(self.awake)

		if lenght == 0:
			self.total_wait_calls += 1

			if all(waker.is_empty() for waker in self.wakers.values()):
				# there is no task left, neither awake nor asleep
				return True
			else:
				# io wakers simply need to return 0 for max_sleep and they will be used for sleeping
				non_empty_wakers = filter(lambda x: not x.is_empty(), self.wakers.values())
				waker, sleep_duration = min(
					((waker, waker.max_sleep()) for waker in non_empty_wakers),
					key=lambda x: x[1],
				)

				if sleep_duration > 0:  # this happens sometimes
					start = now()
					waker.sleep(sleep_duration)
					actual_sleep_duration = start.interval()
					self.total_sleep += actual_sleep_duration

					self.log("{:.6f}, {}, {:.6f}".format(sleep_duration, type(waker).__name__, actual_sleep_duration))
				else:
					pass
					# self.log(f"Negative sleep_duration for {type(waker).__name__}: {sleep_duration}")
		return False

	def clear_wakers(self):
		wakers_to_pop = []
		for waker in self.wakers.values():
			# might use a way to keep track how long the waker stays unused here
			# also we might want to have a list of permanent wakers
			if waker.is_empty():
				wakers_to_pop.append(waker)

		for waker in wakers_to_pop:
			self.wakers.pop(type(waker))

	def run_until_completion(self):
		self.start = now()
		while True:
			stop = self.wait()
			if stop:
				break
			self.run_once()
		dilation = self.start.interval()

		self.log("total steps:", self.step_count)
		self.log("wait on wakers:", self.total_wait_calls)
		self.log("total uptime (seconds): {:.6f}/{:.6f}".format(dilation - self.total_sleep, dilation))

		return dilation

	def close(self, timeout=0):  # TODO: implement timeout
		for waker in self.wakers.values():
			waker.close()
		self.clear_wakers()

		for task in self.awake:
			task.close()

		if self.wakers:
			self.log(self.wakers)
			raise RuntimeError("Couldn't close all wakers")
		if self.awake:
			self.log(self.awake)
			raise RuntimeError("Couldn't close all tasks")

		self.closed = True

	def __del__(self):
		if not self.closed:
			self.close()
			if self.debug:
				raise RuntimeError("The Scheduler is not closed.")

	def mainloop(self, coroutine, wait_for_spawned=True):  # TODO: implement wait_for_spawned (using Task.cancel maybe?)
		task = self.create_task(coroutine)
		task.set_name("{} (mainloop)".format(task.name()))
		self.run_until_completion()
		self.close()
		return task.result_or_raise()

	# TODO: how should this work? wrap it in a task and return perhaps? should it be a coroutine or function?
	def in_new_thread(self, coroutine):
		pass
