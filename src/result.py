class Command:
    (GET, PUT_TO_SLEEP, SWITCH) = range(3)


class StepResult:
    def __init__(self, command, context=None, waker=None):
        self.command = command
        self.waker = waker
        self.context = context

    def __await__(self):
        # return is used for returning the value back to the coroutine
        return (yield self)


result = StepResult
