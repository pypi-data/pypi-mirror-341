import asyncio
import json

from cbpi.api import *
from cbpi.api import CBPiActor, Property, parameters


@parameters([Property.Text(label="Topic", configurable=True, description="MQTT Topic")])
class MQTTActor(CBPiActor):

    # Custom property which can be configured by the user
    @action(
        "Set Power",
        parameters=[
            Property.Number(
                label="Power", configurable=True, description="Power Setting [0-100]"
            )
        ],
    )
    async def setpower(self, Power=100, **kwargs):
        self.power = int(Power)
        if self.power < 0:
            self.power = 0
        if self.power > 100:
            self.power = 100
        await self.set_power(self.power)

    def __init__(self, cbpi, id, props):
        super(MQTTActor, self).__init__(cbpi, id, props)

    async def on_start(self):
        self.topic = self.props.get("Topic", None)
        self.power = 100
        await self.off()
        self.state = False

    async def on(self, power=None):
        if power is not None:
            if power != self.power:
                power = min(100, power)
                power = max(0, power)
                self.power = round(power)
        await self.cbpi.satellite.publish(
            self.topic, json.dumps({"state": "on", "power": self.power}), True
        )
        self.state = True
        pass

    async def off(self):
        self.state = False
        await self.cbpi.satellite.publish(
            self.topic, json.dumps({"state": "off", "power": 0}), True
        )
        pass

    async def run(self):
        while self.running:
            await asyncio.sleep(1)

    def get_state(self):
        return self.state

    async def set_power(self, power):
        self.power = round(power)
        if self.state == True:
            await self.on(power)
        else:
            await self.off()
        await self.cbpi.actor.actor_update(self.id, power)
        pass
