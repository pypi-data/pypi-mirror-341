import logging
from datetime import datetime
from socket import timeout
from typing import KeysView
from unittest.mock import MagicMock, patch

from cbpi.api import *
from cbpi.api.dataclasses import NotificationAction, NotificationType
from voluptuous.schema_builder import message

logger = logging.getLogger(__name__)


@parameters([])
class DummyActor(CBPiActor):

    def __init__(self, cbpi, id, props):
        super().__init__(cbpi, id, props)

    @action("SAY HELLO", {})
    async def helloWorld(self, **kwargs):
        self.cbpi.notify("HELLO", "WOOHO", NotificationType.ERROR)

    async def start(self):
        await super().start()

    async def on(self, power=0):
        logger.info("ACTOR %s ON " % self.id)
        self.state = True

    async def off(self):
        logger.info("ACTOR %s OFF " % self.id)

        self.state = False

    def get_state(self):

        return self.state

    async def run(self):
        pass


def setup(cbpi):
    """
    This method is called by the server during startup
    Here you need to register your plugins at the server

    :param cbpi: the cbpi core
    :return:
    """

    cbpi.plugin.register("DummyActor", DummyActor)
