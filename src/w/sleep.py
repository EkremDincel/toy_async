from .waker import AbstractWaker, context_with_waker
from time import time
import heapq


class WakerSleep(AbstractWaker):
    def __init__(self):
        self.sleeping = []
        self.sleeping_sequence = 0

    def __call__(self, ready):
        while self.sleeping:
            deadline, sequence, function = heapq.heappop(self.sleeping)
            delta = deadline - time()
            if delta > 0:
                heapq.heappush(self.sleeping, (deadline, sequence, function))
                return
            ready((function, None))

    def schedule(self, function, context, ready):
        self.sleeping_sequence += 1
        deadline = time() + context
        heapq.heappush(self.sleeping, (deadline, self.sleeping_sequence, function))

    def max_sleep(self):
        if self.is_empty():
            return float("inf")
        return self.sleeping[0][0] - time()

    def is_empty(self):
        return not self.sleeping

    def close(self):
        pass

    def __repr__(self):
        return repr(self.sleeping)


sleep = context_with_waker(WakerSleep)
