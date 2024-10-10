from toy_async import *
from functools import wraps, partial


class Repeater:
    def __init__(self):
        self.scheduler = Scheduler()

    def repeat(self, interval, function, delay=0, count=float("inf")):
        @wraps(function)
        async def waiter():
            await sleep(delay)
            if count <= 0:
                return

            current = 0
            while True:
                result = function()
                if result is not None and result == False:
                    break

                current += 1
                if not current < count:
                    break
                await sleep(interval)

        self.scheduler.create_task(waiter())

    def run(self):
        self.scheduler.run_until_completion()


r = Repeater()
r.repeat(1, partial(print, "Hello", end="", flush=True), count=5)
r.repeat(1, partial(print, " World!"), delay=0.5, count=5)
r.run()
