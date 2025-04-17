import asyncio
import logging
import time
import warnings
from datetime import datetime
from socket import timeout
from typing import KeysView

import numpy as np
from cbpi.api import *
from cbpi.api import Property, action, parameters
from cbpi.api.base import CBPiBase
from cbpi.api.config import ConfigType
from cbpi.api.dataclasses import (
    Fermenter,
    Kettle,
    NotificationAction,
    NotificationType,
    Props,
)
from cbpi.api.step import CBPiFermentationStep, StepResult
from cbpi.api.timer import Timer
from voluptuous.schema_builder import message


@parameters(
    [
        Property.Text(
            label="Notification", configurable=True, description="Text for notification"
        ),
        Property.Select(
            label="AutoNext",
            options=["Yes", "No"],
            description="Automatically move to next step (Yes) or pause after Notification (No)",
        ),
    ]
)
class FermenterNotificationStep(CBPiFermentationStep):

    async def NextStep(self, **kwargs):
        await self.next(self.fermenter.id)
        return StepResult.DONE

    async def on_timer_done(self, timer):
        self.summary = self.props.get("Notification", "")

        if self.AutoNext == True:
            self.cbpi.notify(
                self.name, self.props.get("Notification", ""), NotificationType.INFO
            )
            if self.shutdown != True:
                await self.next(self.fermenter.id)
                return StepResult.DONE
        else:
            self.cbpi.notify(
                self.name,
                self.props.get("Notification", ""),
                NotificationType.INFO,
                action=[NotificationAction("Next Step", self.NextStep)],
            )
            await self.push_update()

    async def on_timer_update(self, timer, seconds):
        await self.push_update()

    async def on_start(self):
        self.shutdown = False
        self.summary = ""
        self.AutoNext = False if self.props.get("AutoNext", "No") == "No" else True
        if self.timer is None:
            self.timer = Timer(
                1, on_update=self.on_timer_update, on_done=self.on_timer_done
            )
        await self.push_update()

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        await self.push_update()

    async def run(self):
        while self.running == True:
            await asyncio.sleep(1)
            if self.timer.is_running is not True:
                self.timer.start()
                self.timer.is_running = True

        return StepResult.DONE


@parameters(
    [
        Property.Number(label="Temp", configurable=True),
        Property.Sensor(label="Sensor"),
        Property.Text(
            label="Notification",
            configurable=True,
            description="Text for notification when Temp is reached",
        ),
        Property.Select(
            label="AutoMode",
            options=["Yes", "No"],
            description="Switch Fermenterlogic automatically on and off -> Yes",
        ),
    ]
)
class FermenterTargetTempStep(CBPiFermentationStep):

    async def NextStep(self, **kwargs):
        if self.shutdown != True:
            await self.next(self.fermenter.id)
            return StepResult.DONE

    async def on_timer_done(self, timer):
        self.summary = ""
        await self.push_update()
        if self.AutoMode == True:
            await self.setAutoMode(False)
        self.cbpi.notify(
            self.name,
            self.props.get(
                "Notification",
                "Target Temp reached. Please add malt and klick next to move on.",
            ),
        )
        if self.shutdown == False:
            await self.next(self.fermenter.id)
            return StepResult.DONE

    async def on_timer_update(self, timer, seconds):
        await self.push_update()

    async def on_start(self):
        self.shutdown = False
        self.AutoMode = True if self.props.get("AutoMode", "No") == "Yes" else False
        if self.fermenter is not None:
            self.fermenter.target_temp = float(self.props.get("Temp", 0))
            self.fermenter.target_pressure = 0
        if self.AutoMode == True:
            await self.setAutoMode(True)
        self.summary = "Waiting for Target Temp"
        if self.fermenter is not None and self.timer is None:
            self.timer = Timer(
                1, on_update=self.on_timer_update, on_done=self.on_timer_done
            )
        await self.push_update()

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        if self.AutoMode == True:
            await self.setAutoMode(False)
        await self.push_update()

    async def run(self):
        while self.get_sensor_value(self.props.get("Sensor", None)).get("value") > 900:
            await asyncio.sleep(1)
        self.starttemp = self.get_sensor_value(self.props.get("Sensor", None)).get(
            "value"
        )
        if self.fermenter.target_temp >= self.starttemp:
            logging.info("warmup")
            while self.running == True:
                sensor_value = self.get_sensor_value(
                    self.props.get("Sensor", None)
                ).get("value")
                if (
                    sensor_value >= self.fermenter.target_temp
                    and self.timer.is_running is not True
                ):
                    self.timer.start()
                    self.timer.is_running = True
                await asyncio.sleep(1)
        elif self.fermenter.target_temp <= self.starttemp:
            logging.info("Cooldown")
            while self.running == True:
                sensor_value = self.get_sensor_value(
                    self.props.get("Sensor", None)
                ).get("value")
                if (
                    sensor_value <= self.fermenter.target_temp
                    and self.timer.is_running is not True
                ):
                    self.timer.start()
                    self.timer.is_running = True
                await asyncio.sleep(1)
        await self.push_update()
        return StepResult.DONE

    async def reset(self):
        self.timer = Timer(
            1, on_update=self.on_timer_update, on_done=self.on_timer_done
        )
        self.timer.is_running == False

    async def setAutoMode(self, auto_state):
        try:
            if (
                self.fermenter.instance is None
                or self.fermenter.instance.state == False
            ) and (auto_state is True):
                await self.cbpi.fermenter.toggle(self.fermenter.id)
            elif (self.fermenter.instance.state == True) and (auto_state is False):
                await self.cbpi.fermenter.toggle(self.fermenter.id)
            await self.push_update()

        except Exception as e:
            logging.error(
                "Failed to switch on FermenterLogic {} {}".format(self.fermenter.id, e)
            )


@parameters(
    [
        Property.Number(label="TimerD", description="Timer Days", configurable=True),
        Property.Number(label="TimerH", description="Timer Hours", configurable=True),
        Property.Number(label="TimerM", description="Timer Minutes", configurable=True),
        Property.Number(
            label="Temp", configurable=True, description="Step Temperature"
        ),
        Property.Number(
            label="Pressure", configurable=True, description="Step Pressure"
        ),
        Property.Sensor(label="Sensor", description="Temperature Sensor"),
        Property.Select(
            label="AutoMode",
            options=["Yes", "No"],
            description="Switch Fermenterlogic automatically on and off -> Yes",
        ),
    ]
)
class FermenterStep(CBPiFermentationStep):

    @action("Start Timer", [])
    async def start_timer(self):
        if self.timer.is_running is not True:
            self.cbpi.notify(self.name, "Timer started", NotificationType.INFO)
            self.timer.start()
            self.timer.is_running = True
            self.endtime = time.time() + self.fermentationtime
            await self.update_endtime()
            estimated_completion_time = datetime.fromtimestamp(
                time.time() + self.fermentationtime
            )
            self.cbpi.notify(
                self.name,
                "Timer started. Estimated completion: {}".format(
                    estimated_completion_time.strftime("%d.%m, %H:%M")
                ),
                NotificationType.INFO,
            )
        else:
            self.cbpi.notify(
                self.name, "Timer is already running", NotificationType.WARNING
            )

    #    @action("Add 1 Day to Timer", [])
    #    async def add_timer(self):
    #        if self.timer.is_running == True:
    #            self.cbpi.notify(self.name, '1 Day added', NotificationType.INFO)
    #            await self.timer.add(86400)
    #            self.endtime = self.endtime +86400
    #            await self.update_endtime()
    #        else:
    #            self.cbpi.notify(self.name, 'Timer must be running to add time', NotificationType.WARNING)

    async def on_timer_done(self, timer):
        self.summary = ""
        if self.AutoMode == True:
            await self.setAutoMode(False)
        self.cbpi.notify(self.name, "Step finished", NotificationType.SUCCESS)
        if self.shutdown == False:
            await self.next(self.fermenter.id)
            return StepResult.DONE

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        await self.push_update()

    async def on_start(self):
        self.shutdown = False
        if self.endtime == 0:
            timeD = int(self.props.get("TimerD", 0))
            timeH = int(self.props.get("TimerH", 0))
            timeM = int(self.props.get("TimerM", 0))
            self.fermentationtime = (timeM + (60 * timeH) + (1440 * timeD)) * 60
        else:
            self.fermentationtime = self.endtime - time.time()

        self.AutoMode = True if self.props.get("AutoMode", "No") == "Yes" else False
        if self.fermenter is not None:
            self.fermenter.target_temp = float(self.props.get("Temp", 0))
            self.fermenter.target_pressure = float(self.props.get("Pressure", 0))
        if self.AutoMode == True:
            await self.setAutoMode(True)
        await self.push_update()

        if self.fermenter is not None and self.timer is None:
            logging.info("Set Timer")
            self.timer = Timer(
                self.fermentationtime,
                on_update=self.on_timer_update,
                on_done=self.on_timer_done,
            )
            self.timer.is_running = False
        elif self.fermenter is not None:
            try:
                if self.timer.is_running == True:
                    self.timer.start()
                    self.endtime = time.time() + self.fermentationtime
                    await self.update_endtime()
            except:
                pass

        if (
            self.endtime != 0
            and self.timer is not None
            and self.timer.is_running == False
        ):
            self.timer.start()
            self.timer.is_running = True
            estimated_completion_time = datetime.fromtimestamp(
                time.time() + self.fermentationtime
            )
            self.cbpi.notify(
                self.name,
                "Timer restarted. Estimated completion: {}".format(
                    estimated_completion_time.strftime("%d.%m, %H:%M")
                ),
                NotificationType.INFO,
            )

        self.summary = "Waiting for Target Temp"
        await self.push_update()

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        if self.AutoMode == True:
            await self.setAutoMode(False)
        await self.push_update()

    async def reset(self):
        timeD = int(self.props.get("TimerD", 0))
        timeH = int(self.props.get("TimerH", 0))
        timeM = int(self.props.get("TimerM", 0))
        self.fermentationtime = (timeM + (60 * timeH) + (1440 * timeD)) * 60
        self.timer = Timer(
            self.fermentationtime,
            on_update=self.on_timer_update,
            on_done=self.on_timer_done,
        )
        self.endtime = 0
        self.timer.is_running == False

    async def run(self):
        while self.get_sensor_value(self.props.get("Sensor", None)).get("value") > 900:
            await asyncio.sleep(1)
        self.starttemp = self.get_sensor_value(self.props.get("Sensor", None)).get(
            "value"
        )

        if self.fermenter.target_temp >= self.starttemp:
            logging.info("warmup")
            while self.running == True:
                await asyncio.sleep(1)
                sensor_value = self.get_sensor_value(
                    self.props.get("Sensor", None)
                ).get("value")
                if (
                    sensor_value >= self.fermenter.target_temp
                    and self.timer.is_running is not True
                ):
                    self.timer.start()
                    self.timer.is_running = True
                    self.endtime = time.time() + self.fermentationtime
                    await self.update_endtime()
                    estimated_completion_time = datetime.fromtimestamp(
                        time.time() + self.fermentationtime
                    )
                    self.cbpi.notify(
                        self.name,
                        "Timer started. Estimated completion: {}".format(
                            estimated_completion_time.strftime("%d.%m, %H:%M")
                        ),
                        NotificationType.INFO,
                    )
        elif self.fermenter.target_temp <= self.starttemp:
            logging.info("cooldown")
            while self.running == True:
                await asyncio.sleep(1)
                sensor_value = self.get_sensor_value(
                    self.props.get("Sensor", None)
                ).get("value")
                if (
                    sensor_value <= self.fermenter.target_temp
                    and self.timer.is_running is not True
                ):
                    self.timer.start()
                    self.timer.is_running = True
                    self.endtime = time.time() + self.fermentationtime
                    await self.update_endtime()
                    estimated_completion_time = datetime.fromtimestamp(
                        time.time() + self.fermentationtime
                    )
                    self.cbpi.notify(
                        self.name,
                        "Timer started. Estimated completion: {}".format(
                            estimated_completion_time.strftime("%d.%m, %H:%M")
                        ),
                        NotificationType.INFO,
                    )

        return StepResult.DONE

    async def setAutoMode(self, auto_state):
        try:
            if (
                self.fermenter.instance is None
                or self.fermenter.instance.state == False
            ) and (auto_state is True):
                await self.cbpi.fermenter.toggle(self.fermenter.id)
            elif (self.fermenter.instance.state == True) and (auto_state is False):
                await self.cbpi.fermenter.toggle(self.fermenter.id)
            await self.push_update()

        except Exception as e:
            logging.error(
                "Failed to switch on FermenterLogic {} {}".format(self.fermenter.id, e)
            )


@parameters(
    [
        Property.Number(
            label="Temp", configurable=True, description="Ramp to this temp"
        ),
        Property.Number(
            label="Pressure", configurable=True, description="Step Pressure"
        ),
        Property.Number(
            label="RampRate",
            configurable=True,
            description="Ramp x °C/F per  day. Default: 1",
        ),
        Property.Sensor(label="Sensor", description="Temperature Sensor"),
        Property.Text(
            label="Notification",
            configurable=True,
            description="Text for notification when Temp is reached",
        ),
        Property.Select(
            label="AutoMode",
            options=["Yes", "No"],
            description="Switch Fermenterlogic automatically on and off -> Yes",
        ),
    ]
)
class FermenterRampTempStep(CBPiFermentationStep):

    async def NextStep(self, **kwargs):
        if self.shutdown == False:
            await self.next(self.fermenter.id)
            return StepResult.DONE

    async def on_timer_done(self, timer):
        self.summary = ""
        await self.push_update()
        if self.AutoMode == True:
            await self.setAutoMode(False)
        self.cbpi.notify(
            self.name,
            self.props.get(
                "Notification",
                "Target Temp reached. Please add malt and klick next to move on.",
            ),
        )
        await self.next(self.fermenter.id)
        return StepResult.DONE

    async def on_timer_update(self, timer, seconds):
        await self.push_update()

    async def on_start(self):
        self.shutdown = False
        self.AutoMode = True if self.props.get("AutoMode", "No") == "Yes" else False
        self.rate = float(self.props.get("RampRate", 1))
        logging.info(self.rate)
        self.target_temp = round(float(self.props.get("Temp", 0)) * 10) / 10
        logging.info(self.target_temp)
        self.fermenter.target_pressure = float(self.props.get("Pressure", 0))
        while self.get_sensor_value(self.props.get("Sensor", None)).get("value") > 900:
            await asyncio.sleep(1)
        self.starttemp = self.get_sensor_value(self.props.get("Sensor", None)).get(
            "value"
        )

        self.current_target_temp = self.starttemp
        if self.fermenter is not None:
            await self.set_fermenter_target_temp(
                self.fermenter.id, self.current_target_temp
            )
        if self.AutoMode == True:
            await self.setAutoMode(True)
        self.summary = "Ramping to {}° with {}° per day".format(
            self.target_temp, self.rate
        )
        if self.fermenter is not None and self.timer is None:
            self.timer = Timer(
                1, on_update=self.on_timer_update, on_done=self.on_timer_done
            )
        await self.push_update()

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        if self.AutoMode == True:
            await self.setAutoMode(False)
        await self.push_update()

    async def calc_target_temp(self):
        delta_time = time.time() - self.starttime
        current_target_temp = (
            round((self.starttemp + delta_time * self.ratesecond) * 10) / 10
        )
        #        logging.info(current_target_temp)
        if current_target_temp != self.current_target_temp:
            self.current_target_temp = current_target_temp
            await self.set_fermenter_target_temp(
                self.fermenter.id, self.current_target_temp
            )
            # self.fermenter.target_temp = self.current_target_temp
            await self.push_update()

        pass

    async def run(self):
        self.delta_temp = self.target_temp - self.starttemp
        try:
            self.deltadays = abs(self.delta_temp / self.rate)
            self.deltaseconds = self.deltadays * 24 * 60 * 60
            self.ratesecond = self.delta_temp / self.deltaseconds
        except Exception as e:
            logging.info(e)
        self.starttime = time.time()

        if self.target_temp >= self.starttemp:
            logging.info("warmup")
            while self.running == True:
                if self.current_target_temp != self.target_temp:
                    await self.calc_target_temp()
                sensor_value = self.get_sensor_value(
                    self.props.get("Sensor", None)
                ).get("value")
                if (
                    sensor_value >= self.target_temp
                    and self.timer.is_running is not True
                ):
                    self.timer.start()
                    self.timer.is_running = True
                await asyncio.sleep(1)
        elif self.target_temp <= self.starttemp:
            logging.info("Cooldown")
            while self.running == True:
                if self.current_target_temp != self.target_temp:
                    await self.calc_target_temp()
                sensor_value = self.get_sensor_value(
                    self.props.get("Sensor", None)
                ).get("value")
                if (
                    sensor_value <= self.target_temp
                    and self.timer.is_running is not True
                ):
                    self.timer.start()
                    self.timer.is_running = True
                await asyncio.sleep(1)
        await self.push_update()
        return StepResult.DONE

    async def reset(self):
        self.timer = Timer(
            1, on_update=self.on_timer_update, on_done=self.on_timer_done
        )
        self.timer.is_running == False

    async def setAutoMode(self, auto_state):
        try:
            if (
                self.fermenter.instance is None
                or self.fermenter.instance.state == False
            ) and (auto_state is True):
                await self.cbpi.fermenter.toggle(self.fermenter.id)
            elif (self.fermenter.instance.state == True) and (auto_state is False):
                await self.fermenter.instance.stop()
            await self.push_update()

        except Exception as e:
            logging.error(
                "Failed to switch on FermenterLogic {} {}".format(self.fermenter.id, e)
            )


def setup(cbpi):
    """
    This method is called by the server during startup
    Here you need to register your plugins at the server

    :param cbpi: the cbpi core
    :return:
    """

    cbpi.plugin.register("FermenterNotificationStep", FermenterNotificationStep)
    cbpi.plugin.register("FermenterTargetTempStep", FermenterTargetTempStep)
    cbpi.plugin.register("FermenterRampTempStep", FermenterRampTempStep)
    cbpi.plugin.register("FermenterStep", FermenterStep)
