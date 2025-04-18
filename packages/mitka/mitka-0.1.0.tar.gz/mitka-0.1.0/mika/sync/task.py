import random
import threading


class KWTaskStopped(BaseException):
    def __init__(self, reason: str | None):
        super().__init__()
        self.reason = reason


class TaskToken:
    def __init__(self):
        self.ev = threading.Event()

    def sleep(self, sec: float, reason: str | None = None):
        if self.ev.wait(sec):
            raise KWTaskStopped(reason)

    def rsleep(self, sec: float, random_min: float = 0.5, random_max: float = 0.7):
        self.sleep(sec + random.uniform(random_min, random_max))
