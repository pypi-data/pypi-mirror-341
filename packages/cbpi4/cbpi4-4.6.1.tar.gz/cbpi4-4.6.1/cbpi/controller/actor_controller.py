import logging

from cbpi.api.dataclasses import Actor
from cbpi.controller.basic_controller2 import BasicController
from tabulate import tabulate


class ActorController(BasicController):

    def __init__(self, cbpi):
        super(ActorController, self).__init__(cbpi, Actor, "actor.json")
        self.update_key = "actorupdate"
        self.sorting = True

    async def on(self, id, power=None):
        try:
            item = self.find_by_id(id)
            if power is None:
                logging.info("Power is none")
                if item.power:
                    power = item.power
                else:
                    power = 100
            if item.instance.state is False:
                await item.instance.on(power)
                # await self.push_udpate()
                self.cbpi.ws.send(
                    dict(
                        topic=self.update_key,
                        data=list(map(lambda item: item.to_dict(), self.data)),
                    ),
                    self.sorting,
                )
                self.cbpi.push_update(
                    "cbpi/actorupdate/{}".format(id), item.to_dict(), True
                )
            else:
                await self.set_power(id, power)

        except Exception as e:
            logging.error("Failed to switch on Actor {} {}".format(id, e))

    async def off(self, id):
        try:
            item = self.find_by_id(id)
            if item.instance.state is True:
                await item.instance.off()
                # await self.push_udpate()
                self.cbpi.ws.send(
                    dict(
                        topic=self.update_key,
                        data=list(map(lambda item: item.to_dict(), self.data)),
                    ),
                    self.sorting,
                )
                self.cbpi.push_update("cbpi/actorupdate/{}".format(id), item.to_dict())
        except Exception as e:
            logging.error("Failed to switch on Actor {} {}".format(id, e), True)

    async def toogle(self, id):
        try:
            item = self.find_by_id(id)
            instance = item.get("instance")
            await instance.toggle()
            self.cbpi.ws.send(
                dict(
                    topic=self.update_key,
                    data=list(map(lambda item: item.to_dict(), self.data)),
                ),
                self.sorting,
            )
            self.cbpi.push_update("cbpi/actorupdate/{}".format(id), item.to_dict())
        except Exception as e:
            logging.error("Failed to toggle Actor {} {}".format(id, e))

    async def set_power(self, id, power):
        try:
            item = self.find_by_id(id)
            await item.instance.set_power(power)
        except Exception as e:
            logging.error("Failed to set power {} {}".format(id, e))

    async def actor_update(self, id, power):
        try:
            item = self.find_by_id(id)
            item.power = round(power)
            # await self.push_udpate()
            self.cbpi.ws.send(
                dict(
                    topic=self.update_key,
                    data=list(map(lambda item: item.to_dict(), self.data)),
                ),
                self.sorting,
            )
            self.cbpi.push_update("cbpi/actorupdate/{}".format(id), item.to_dict())
        except Exception as e:
            logging.error("Failed to update Actor {} {}".format(id, e))

    async def timeractor_update(self, id, timer):
        try:
            item = self.find_by_id(id)
            item.timer = round(timer)
            # await self.push_udpate()
            self.cbpi.ws.send(
                dict(
                    topic=self.update_key,
                    data=list(map(lambda item: item.to_dict(), self.data)),
                )
            )
            self.cbpi.push_update("cbpi/actorupdate/{}".format(id), item.to_dict())
        except Exception as e:
            logging.error("Failed to update Actor {} {}".format(id, e))

    async def ws_actor_update(self):
        try:
            # await self.push_udpate()
            self.cbpi.ws.send(
                dict(
                    topic=self.update_key,
                    data=list(map(lambda x: x.to_dict(), self.data)),
                ),
                self.sorting,
            )
        #            self.cbpi.push_update("cbpi/actorupdate/{}".format(id), item.to_dict())
        except Exception as e:
            logging.error("Failed to update Actors {}".format(e))
