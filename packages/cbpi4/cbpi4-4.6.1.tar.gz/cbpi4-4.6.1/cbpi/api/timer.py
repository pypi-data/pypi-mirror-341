import asyncio
import math
import time


class Timer(object):

    def __init__(self, timeout, on_done=None, on_update=None) -> None:
        super().__init__()
        self.timeout = timeout
        self._timemout = self.timeout
        self._task = None
        self._callback = on_done
        self._update = on_update
        self.start_time = None
        self.end_time = None

    def done(self, task):
        if self._callback is not None:
            asyncio.create_task(self._callback(self))

    async def _job(self):
        self.start_time = int(time.time())
        self.end_time = self.start_time + int(round(self._timemout, 0))
        self.count = self.end_time - self.start_time
        try:
            while self.count > 0:
                self.count = self.end_time - int(time.time())
                if self._update is not None:
                    await self._update(self, self.count)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            end = int(time.time())
            duration = end - self.start_time
            self._timemout = self._timemout - duration

    async def add(self, seconds):
        self.end_time = self.end_time + seconds

    def start(self):
        self._task = asyncio.create_task(self._job())
        self._task.add_done_callback(self.done)

    async def stop(self):
        if self._task and self._task.done() is False:
            self._task.cancel()
            await self._task

    def reset(self):
        if self.is_running is True:
            return
        self._timemout = self.timeout

    def is_running(self):
        return not self._task.done()

    def set_time(self, timeout):
        if self.is_running is True:
            return
        self.timeout = timeout

    def get_time(self):
        return self.format_time(int(round(self._timemout, 0)))

    @classmethod
    def format_time(cls, time):
        pattern_h = "{0:02d}:{1:02d}:{2:02d}"
        pattern_d = "{0:02d}D {1:02d}:{2:02d}:{3:02d}"
        seconds = time % 60
        minutes = math.floor(time / 60) % 60
        hours = math.floor(time / 3600) % 24
        days = math.floor(time / 86400)
        if days != 0:
            remaining_time = pattern_d.format(days, hours, minutes, seconds)
        else:
            remaining_time = pattern_h.format(hours, minutes, seconds)
        return remaining_time
