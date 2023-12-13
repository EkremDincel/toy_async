from .commands import switch

class Task:
	def __init__(self, coroutine):
		self.coroutine = coroutine
		self.finished = False
		self.result = None

	def set(self, result):
		self.finished = True
		self.result = result

	async def join(self):
		pass