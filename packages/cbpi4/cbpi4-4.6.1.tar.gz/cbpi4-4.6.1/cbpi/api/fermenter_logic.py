import asyncio
import logging
from abc import ABCMeta

from cbpi.api.base import CBPiBase
from cbpi.api.extension import CBPiExtension


class CBPiFermenterLogic(CBPiBase, metaclass=ABCMeta):

    def __init__(self, cbpi, id, props):
        self.cbpi = cbpi
        self.id = id
        self.props = props
        self.state = False
        self.running = False

    def init(self):
        pass

    async def on_start(self):
        pass

    async def on_stop(self):
        pass

    async def run(self):
        pass

    async def _run(self):

        try:
            await self.on_start()
            self.cancel_reason = await self.run()
        except asyncio.CancelledError as e:
            pass
        finally:
            await self.on_stop()

    def get_state(self):
        return dict(running=self.state)

    async def start(self):

        self.state = True

    async def stop(self):

        self.task.cancel()
        await self.task
        self.state = False
