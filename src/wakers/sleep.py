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

    def max_sleep(self):
        if self.is_empty():
            return float("inf")
        return self.sleeping[0][0] - timer()

    def is_empty(self):
        return not self.sleeping

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
        pass

    def __repr__(self):
        return repr(self.sleeping)
