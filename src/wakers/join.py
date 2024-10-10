from ..commands import put_to_sleep
from .waker import AbstractWaker

__all__ = ["join"]


def join(tasks):
    return put_to_sleep(WakerJoin, tasks)


class WakerJoin(AbstractWaker):
    def __init__(self, awaken):
        self.awaken = awaken
        self.joined = {}

    def __call__(self):
        tasks_to_awake = []

        for task, joined_on in self.joined.items():
            if all(t.finished() for t in joined_on):
                self.awaken((task, (i.result() for i in joined_on)))
                tasks_to_awake.append(task)

        for t in tasks_to_awake:
            self.joined.pop(t)

    def schedule(self, task, context):
        self.joined[task] = context

    def max_sleep(self):
        # TODO: hata burada
        return float("inf")

    def is_empty(self):
        return not self.joined

    def sleep(self, time):
        pass

    def close(self):
        pass

    def __repr__(self):
        return repr(self.sleeping)
