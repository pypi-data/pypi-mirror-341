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
from cbpi.api.dataclasses import Kettle, NotificationAction, NotificationType, Props
from cbpi.api.step import CBPiStep, StepResult
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
class NotificationStep(CBPiStep):

    async def NextStep(self, **kwargs):
        await self.next()

    async def on_timer_done(self, timer):
        self.summary = self.props.get("Notification", "")

        if self.AutoNext == True:
            self.cbpi.notify(
                self.name, self.props.get("Notification", ""), NotificationType.INFO
            )
            await self.next()
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
        Property.Kettle(label="Kettle"),
        Property.Text(
            label="Notification",
            configurable=True,
            description="Text for notification when Temp is reached",
        ),
        Property.Select(
            label="AutoMode",
            options=["Yes", "No"],
            description="Switch Kettlelogic automatically on and off -> Yes",
        ),
    ]
)
class MashInStep(CBPiStep):

    async def NextStep(self, **kwargs):
        await self.next()

    async def on_timer_done(self, timer):
        self.summary = ""
        self.kettle.target_temp = 0
        await self.push_update()
        if self.AutoMode == True:
            await self.setAutoMode(False)
        self.cbpi.notify(
            self.name,
            self.props.get(
                "Notification",
                "Target Temp reached. Please add malt and klick next to move on.",
            ),
            action=[NotificationAction("Next Step", self.NextStep)],
        )

    async def on_timer_update(self, timer, seconds):
        await self.push_update()

    async def on_start(self):
        self.AutoMode = True if self.props.get("AutoMode", "No") == "Yes" else False
        self.kettle = self.get_kettle(self.props.get("Kettle", None))
        if self.kettle is not None:
            self.kettle.target_temp = int(self.props.get("Temp", 0))
        if self.AutoMode == True:
            await self.setAutoMode(True)
        self.summary = "Waiting for Target Temp"
        if self.cbpi.kettle is not None and self.timer is None:
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
        while self.running == True:
            await asyncio.sleep(1)
            sensor_value = self.get_sensor_value(self.props.get("Sensor", None)).get(
                "value"
            )
            if (
                sensor_value >= int(self.props.get("Temp", 0))
                and self.timer.is_running is not True
            ):
                self.timer.start()
                self.timer.is_running = True
        await self.push_update()
        return StepResult.DONE

    async def reset(self):
        self.timer = Timer(
            1, on_update=self.on_timer_update, on_done=self.on_timer_done
        )

    async def setAutoMode(self, auto_state):
        try:
            if (
                self.kettle.instance is None or self.kettle.instance.state == False
            ) and (auto_state is True):
                await self.cbpi.kettle.toggle(self.kettle.id)
            elif (self.kettle.instance.state == True) and (auto_state is False):
                await self.cbpi.kettle.stop(self.kettle.id)
            await self.push_update()

        except Exception as e:
            logging.error(
                "Failed to switch on KettleLogic {} {}".format(self.kettle.id, e)
            )


@parameters(
    [
        Property.Number(
            label="Timer", description="Time in Minutes", configurable=True
        ),
        Property.Number(label="Temp", configurable=True),
        Property.Sensor(label="Sensor"),
        Property.Kettle(label="Kettle"),
        Property.Select(
            label="AutoMode",
            options=["Yes", "No"],
            description="Switch Kettlelogic automatically on and off -> Yes",
        ),
    ]
)
class MashStep(CBPiStep):

    @action("Start Timer", [])
    async def start_timer(self):
        if self.timer.is_running is not True:
            self.cbpi.notify(self.name, "Timer started", NotificationType.INFO)
            self.timer.start()
            self.timer.is_running = True
        else:
            self.cbpi.notify(
                self.name, "Timer is already running", NotificationType.WARNING
            )

    @action("Add 5 Minutes to Timer", [])
    async def add_timer(self):
        if self.timer.is_running == True:
            self.cbpi.notify(self.name, "5 Minutes added", NotificationType.INFO)
            await self.timer.add(300)
        else:
            self.cbpi.notify(
                self.name, "Timer must be running to add time", NotificationType.WARNING
            )

    async def on_timer_done(self, timer):
        self.summary = ""
        self.kettle.target_temp = 0
        if self.AutoMode == True:
            await self.setAutoMode(False)
        self.cbpi.notify(self.name, "Step finished", NotificationType.SUCCESS)

        await self.next()

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        await self.push_update()

    async def on_start(self):
        self.AutoMode = True if self.props.get("AutoMode", "No") == "Yes" else False
        self.kettle = self.get_kettle(self.props.Kettle)
        if self.kettle is not None:
            self.kettle.target_temp = int(self.props.get("Temp", 0))
        if self.AutoMode == True:
            await self.setAutoMode(True)
        await self.push_update()

        if self.cbpi.kettle is not None and self.timer is None:
            self.timer = Timer(
                int(self.props.get("Timer", 0)) * 60,
                on_update=self.on_timer_update,
                on_done=self.on_timer_done,
            )
        elif self.cbpi.kettle is not None:
            try:
                if self.timer.is_running == True:
                    self.timer.start()
            except:
                pass

        self.summary = "Waiting for Target Temp"
        await self.push_update()

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        if self.AutoMode == True:
            await self.setAutoMode(False)
        await self.push_update()

    async def reset(self):
        self.timer = Timer(
            int(self.props.get("Timer", 0)) * 60,
            on_update=self.on_timer_update,
            on_done=self.on_timer_done,
        )

    async def run(self):
        while self.running == True:
            await asyncio.sleep(1)
            sensor_value = self.get_sensor_value(self.props.get("Sensor", None)).get(
                "value"
            )
            if (
                sensor_value >= int(self.props.get("Temp", 0))
                and self.timer.is_running is not True
            ):
                self.timer.start()
                self.timer.is_running = True
                estimated_completion_time = datetime.fromtimestamp(
                    time.time() + (int(self.props.get("Timer", 0))) * 60
                )
                self.cbpi.notify(
                    self.name,
                    "Timer started. Estimated completion: {}".format(
                        estimated_completion_time.strftime("%H:%M")
                    ),
                    NotificationType.INFO,
                )
        return StepResult.DONE

    async def setAutoMode(self, auto_state):
        try:
            if (
                self.kettle.instance is None or self.kettle.instance.state == False
            ) and (auto_state is True):
                await self.cbpi.kettle.toggle(self.kettle.id)
            elif (self.kettle.instance.state == True) and (auto_state is False):
                await self.cbpi.kettle.stop(self.kettle.id)
            await self.push_update()

        except Exception as e:
            logging.error(
                "Failed to switch on KettleLogic {} {}".format(self.kettle.id, e)
            )


@parameters(
    [Property.Number(label="Timer", description="Time in Minutes", configurable=True)]
)
class WaitStep(CBPiStep):

    async def on_timer_done(self, timer):
        self.summary = ""
        await self.next()

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        await self.push_update()

    async def on_start(self):
        if self.timer is None:
            self.timer = Timer(
                int(self.props.Timer) * 60,
                on_update=self.on_timer_update,
                on_done=self.on_timer_done,
            )
        self.timer.start()

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        await self.push_update()

    async def reset(self):
        self.timer = Timer(
            int(self.props.Timer) * 60,
            on_update=self.on_timer_update,
            on_done=self.on_timer_done,
        )

    async def run(self):
        while self.running == True:
            await asyncio.sleep(1)
        return StepResult.DONE


@parameters(
    [
        Property.Select(
            label="toggle_type",
            options=["On", "Off"],
            description="Choose if Actor should be switched on or off in this step",
        ),
        Property.Actor(
            label="Actor", description="Actor that should be toggled during this step"
        ),
    ]
)
class ToggleStep(CBPiStep):
    async def on_timer_done(self, timer):
        self.summary = ""
        await self.next()

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        await self.push_update()

    async def on_start(self):
        if self.timer is None:
            self.timer = Timer(
                1, on_update=self.on_timer_update, on_done=self.on_timer_done
            )
        self.timer.start()
        self.type = self.props.get("toggle_type", "Off")
        self.Actor = self.props.get("Actor", None)
        if self.Actor is not None and self.type == "On":
            await self.actor_on(self.Actor)
        if self.Actor is not None and self.type == "Off":
            await self.actor_off(self.Actor)

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        await self.push_update()

    async def reset(self):
        self.timer = Timer(
            1, on_update=self.on_timer_update, on_done=self.on_timer_done
        )

    async def run(self):
        while self.running == True:
            await asyncio.sleep(1)
        return StepResult.DONE


@parameters(
    [
        Property.Number(
            label="Timer", description="Time in Minutes", configurable=True
        ),
        Property.Actor(label="Actor"),
    ]
)
class ActorStep(CBPiStep):
    async def on_timer_done(self, timer):
        self.summary = ""
        await self.next()

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        await self.push_update()

    async def on_start(self):
        if self.timer is None:
            self.timer = Timer(
                int(self.props.Timer) * 60,
                on_update=self.on_timer_update,
                on_done=self.on_timer_done,
            )
        self.timer.start()
        await self.actor_on(self.props.Actor)

    async def on_stop(self):
        await self.actor_off(self.props.Actor)
        await self.timer.stop()
        self.summary = ""
        await self.push_update()

    async def reset(self):
        self.timer = Timer(
            int(self.props.Timer) * 60,
            on_update=self.on_timer_update,
            on_done=self.on_timer_done,
        )

    async def run(self):
        while self.running == True:
            await asyncio.sleep(1)
        return StepResult.DONE


@parameters(
    [
        Property.Number(
            label="Timer", description="Time in Minutes", configurable=True
        ),
        Property.Number(
            label="Temp", description="Boil temperature", configurable=True
        ),
        # Property.Number(label="DwellTime", description="Time in minutes (Recommended: 5). If temp is not changing significantly within this time, Timer will start. Defaul:0 disabled", configurable=True),
        Property.Sensor(label="Sensor"),
        Property.Kettle(label="Kettle"),
        Property.Select(
            label="LidAlert",
            options=["Yes", "No"],
            description="Trigger Alert to remove lid if temp is close to boil",
        ),
        Property.Select(
            label="AutoMode",
            options=["Yes", "No"],
            description="Switch Kettlelogic automatically on and off -> Yes",
        ),
        # Property.Select(label="AutoTimer",options=["Yes","No"], description="Start Timer automatically if Temp does not change for 5 Minutes and is above 95C/203F"),
        Property.Select(
            "First_Wort",
            options=["Yes", "No"],
            description="First Wort Hop alert if set to Yes",
        ),
        Property.Text(
            "First_Wort_text",
            configurable=True,
            description="First Wort Hop alert text",
        ),
        Property.Number(
            "Hop_1",
            configurable=True,
            description="First Hop alert (minutes before finish)",
        ),
        Property.Text(
            "Hop_1_text", configurable=True, description="First Hop alert text"
        ),
        Property.Number(
            "Hop_2",
            configurable=True,
            description="Second Hop alert (minutes before finish)",
        ),
        Property.Text(
            "Hop_2_text", configurable=True, description="Second Hop alert text"
        ),
        Property.Number(
            "Hop_3",
            configurable=True,
            description="Third Hop alert (minutes before finish)",
        ),
        Property.Text(
            "Hop_3_text", configurable=True, description="Third Hop alert text"
        ),
        Property.Number(
            "Hop_4",
            configurable=True,
            description="Fourth Hop alert (minutes before finish)",
        ),
        Property.Text(
            "Hop_4_text", configurable=True, description="Fourth Hop alert text"
        ),
        Property.Number(
            "Hop_5",
            configurable=True,
            description="Fifth Hop alert (minutes before finish)",
        ),
        Property.Text(
            "Hop_5_text", configurable=True, description="Fifth Hop alert text"
        ),
        Property.Number(
            "Hop_6",
            configurable=True,
            description="Sixth Hop alert (minutes before finish)",
        ),
        Property.Text(
            "Hop_6_text", configurable=True, description="Sixth Hop alert text"
        ),
    ]
)
class BoilStep(CBPiStep):

    @action("Start Timer", [])
    async def start_timer(self):
        if self.timer.is_running is not True:
            self.cbpi.notify(self.name, "Timer started", NotificationType.INFO)
            self.timer.start()
            self.timer.is_running = True
        else:
            self.cbpi.notify(
                self.name, "Timer is already running", NotificationType.WARNING
            )

    @action("Add 5 Minutes to Timer", [])
    async def add_timer(self):
        if self.timer.is_running == True:
            self.cbpi.notify(self.name, "5 Minutes added", NotificationType.INFO)
            await self.timer.add(300)
        else:
            self.cbpi.notify(
                self.name, "Timer must be running to add time", NotificationType.WARNING
            )

    async def on_timer_done(self, timer):
        self.summary = ""
        self.kettle.target_temp = 0
        if self.AutoMode == True:
            await self.setAutoMode(False)
        self.cbpi.notify(self.name, "Boiling completed", NotificationType.SUCCESS)
        await self.next()

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        self.remaining_seconds = seconds
        await self.push_update()

    async def on_start(self):

        self.lid_temp = 95 if self.get_config_value("TEMP_UNIT", "C") == "C" else 203
        self.lid_flag = True if self.props.get("LidAlert", "No") == "Yes" else False
        self.AutoMode = True if self.props.get("AutoMode", "No") == "Yes" else False
        self.AutoTimer = (
            True if self.cbpi.config.get("BoilAutoTimer", "No") == "Yes" else False
        )
        self.first_wort_hop_flag = False
        self.first_wort_hop = self.props.get("First_Wort", "No")
        self.first_wort_hop_text = self.props.get("First_Wort_text", None)
        self.hops_added = ["", "", "", "", "", ""]
        self.remaining_seconds = None
        self.temparray = np.array([])
        # self.dwelltime=int(self.props.get("DwellTime", 0))*60
        self.dwelltime = (
            5 * 60
        )  # tested with 5 minutes -> not exactly 5 min due to accuracy of asyncio.sleep
        self.deviationlimit = 0.3  # derived from a test
        # logging.warning(self.AutoTimer)
        self.summary2 = None

        self.kettle = self.get_kettle(self.props.get("Kettle", None))
        if self.kettle is not None:
            self.kettle.target_temp = float(self.props.get("Temp", 0))

        if self.cbpi.kettle is not None and self.timer is None:
            self.timer = Timer(
                int(self.props.get("Timer", 0)) * 60,
                on_update=self.on_timer_update,
                on_done=self.on_timer_done,
            )

        elif self.cbpi.kettle is not None:
            try:
                if self.timer.is_running == True:
                    self.timer.start()
            except:
                pass

        self.summary = "Waiting for Target Temp"
        if self.AutoMode == True:
            await self.setAutoMode(True)
        await self.push_update()

    async def next_hop_timer(self):
        hop_timers = []
        for x in range(1, 6):
            try:
                hop = int(self.props.get("Hop_%s" % x, None)) * 60
            except:
                hop = None
            if hop is not None and self.remaining_seconds is not None:
                hop_left = self.remaining_seconds - hop
                if hop_left > 0:
                    hop_timers.append(hop_left)
        if hop_timers:
            next_hop_timer = time.strftime("%H:%M:%S", time.gmtime(min(hop_timers)))
        else:
            next_hop_timer = None
        return next_hop_timer

    async def check_hop_timer(self, number, value, text):
        if value is not None and self.hops_added[number - 1] is not True:
            if self.remaining_seconds != None and self.remaining_seconds <= (
                int(value) * 60 + 1
            ):
                self.hops_added[number - 1] = True
                if text is not None and text != "":
                    self.cbpi.notify(
                        "Hop Alert",
                        "Please add %s (%s)" % (text, number),
                        NotificationType.INFO,
                    )
                else:
                    self.cbpi.notify(
                        "Hop Alert", "Please add Hop %s" % number, NotificationType.INFO
                    )

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        self.summary2 = None
        self.kettle.target_temp = 0
        if self.AutoMode == True:
            await self.setAutoMode(False)
        await self.push_update()

    async def reset(self):
        self.timer = Timer(
            int(self.props.get("Timer", 0)) * 60,
            on_update=self.on_timer_update,
            on_done=self.on_timer_done,
        )

    async def run(self):
        if self.first_wort_hop_flag == False and self.first_wort_hop == "Yes":
            self.first_wort_hop_flag = True
            if self.first_wort_hop_text is not None and self.first_wort_hop_text != "":
                self.cbpi.notify(
                    "First Wort Hop Addition!",
                    "Please add %s for first wort" % self.first_wort_hop_text,
                    NotificationType.INFO,
                )
            else:
                self.cbpi.notify(
                    "First Wort Hop Addition!",
                    "Please add hops for first wort",
                    NotificationType.INFO,
                )

        while self.running == True:
            await asyncio.sleep(1)
            sensor_value = self.get_sensor_value(self.props.get("Sensor", None)).get(
                "value"
            )
            self.temparray = np.append(self.temparray, sensor_value)
            if self.temparray.size > self.dwelltime:
                self.temparray = np.delete(self.temparray, 0)
                deviation = np.std(self.temparray)
                if (
                    (sensor_value >= self.lid_temp)
                    and (deviation <= self.deviationlimit)
                    and (self.AutoTimer is True)
                    and (self.timer.is_running is not True)
                ):
                    self.timer.start()
                    self.timer.is_running = True
                    estimated_completion_time = datetime.fromtimestamp(
                        time.time() + (int(self.props.get("Timer", 0))) * 60
                    )
                    self.cbpi.notify(
                        self.name,
                        "Timer started automatically. Estimated completion: {}".format(
                            estimated_completion_time.strftime("%H:%M")
                        ),
                        NotificationType.INFO,
                    )
                logging.info(
                    "Current: " + str(sensor_value) + " | Dev: " + str(deviation)
                )
            if self.lid_flag == True and sensor_value >= self.lid_temp:
                self.cbpi.notify(
                    "Please remove lid!",
                    "Reached temp close to boiling",
                    NotificationType.INFO,
                )
                self.lid_flag = False

            if (
                sensor_value >= float(self.props.get("Temp", 0))
                and self.timer.is_running is not True
            ):
                self.timer.start()
                self.timer.is_running = True
                estimated_completion_time = datetime.fromtimestamp(
                    time.time() + (int(self.props.get("Timer", 0))) * 60
                )
                self.cbpi.notify(
                    self.name,
                    "Timer started. Estimated completion: {}".format(
                        estimated_completion_time.strftime("%H:%M")
                    ),
                    NotificationType.INFO,
                )
            else:
                if self.timer.is_running:
                    try:
                        nexthoptimer = await self.next_hop_timer()
                        self.summary2 = (
                            "Add Hop in: %s" % nexthoptimer
                            if nexthoptimer is not None
                            else None
                        )
                    except:
                        self.summary2 = None
                for x in range(1, 6):
                    await self.check_hop_timer(
                        x,
                        self.props.get("Hop_%s" % x, None),
                        self.props.get("Hop_%s_text" % x, None),
                    )

        return StepResult.DONE

    async def setAutoMode(self, auto_state):
        try:
            if (
                self.kettle.instance is None or self.kettle.instance.state == False
            ) and (auto_state is True):
                await self.cbpi.kettle.toggle(self.kettle.id)
            elif (self.kettle.instance.state == True) and (auto_state is False):
                await self.cbpi.kettle.stop(self.kettle.id)
            await self.push_update()

        except Exception as e:
            logging.error(
                "Failed to switch on KettleLogic {} {}".format(self.kettle.id, e)
            )


@parameters(
    [
        Property.Number(
            label="Temp",
            configurable=True,
            description="Target temperature for cooldown. Notification will be send when temp is reached and Actor can be triggered",
        ),
        Property.Sensor(
            label="Sensor", description="Sensor that is used during cooldown"
        ),
        Property.Actor(
            label="Actor",
            description="Actor can trigger a valve for the cooldwon to target temperature",
        ),
        Property.Kettle(label="Kettle"),
    ]
)
class CooldownStep(CBPiStep):

    async def on_timer_done(self, timer):
        self.summary = ""
        if self.actor is not None:
            await self.actor_off(self.actor)
        self.cbpi.notify(
            "CoolDown",
            "Wort cooled down. Please transfer to Fermenter.",
            NotificationType.INFO,
        )
        await self.next()

    async def on_timer_update(self, timer, seconds):
        await self.push_update()

    async def on_start(self):
        try:
            warnings.simplefilter("ignore", np.exceptions.RankWarning)
        except Exception as e:
            logging.error(f"Numpy Error: {e}")
        self.temp_array = []
        self.time_array = []
        self.kettle = self.get_kettle(self.props.get("Kettle", None))
        self.actor = self.props.get("Actor", None)
        self.target_temp = int(self.props.get("Temp", 0))
        self.Interval = (
            10  # Interval in minutes on how often cooldwon end time is calculated
        )

        self.cbpi.notify(
            self.name,
            "Cool down to {}°".format(self.target_temp),
            NotificationType.INFO,
        )
        if self.timer is None:
            self.timer = Timer(
                1, on_update=self.on_timer_update, on_done=self.on_timer_done
            )
        self.start_time = time.time()
        self.temp_array.append(
            self.get_sensor_value(self.props.get("Sensor", None)).get("value")
        )
        self.time_array.append(time.time())
        self.next_check = self.start_time + self.Interval * 60
        self.count = 0
        self.initial_date = None

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        if self.actor is not None:
            await self.actor_off(self.actor)
        await self.push_update()

    async def reset(self):
        self.timer = Timer(
            1, on_update=self.on_timer_update, on_done=self.on_timer_done
        )

    async def run(self):
        timestring = datetime.fromtimestamp(self.start_time)
        if self.actor is not None:
            await self.actor_on(self.actor)
        self.summary = "Started: {}".format(timestring.strftime("%H:%M"))
        await self.push_update()
        while self.running == True:
            current_temp = self.get_sensor_value(self.props.get("Sensor", None)).get(
                "value"
            )
            if self.count == 3:
                self.temp_array.append(current_temp)
                current_time = time.time()
                if self.initial_date == None:
                    self.initial_date = current_time
                self.time_array.append(current_time)
                self.count = 0
            if time.time() >= self.next_check:
                self.next_check = time.time() + (self.Interval * 60)

                cooldown_model = np.polynomial.polynomial.Polynomial.fit(
                    self.temp_array, self.time_array, 2
                )
                target_time = cooldown_model(self.target_temp)
                target_timestring = datetime.fromtimestamp(target_time)
                self.summary = "ECT: {}".format(target_timestring.strftime("%H:%M"))
                self.cbpi.notify(
                    "Cooldown Step",
                    "Current: {}°, reaching {}° at {}".format(
                        round(current_temp, 1),
                        self.target_temp,
                        target_timestring.strftime("%d.%m %H:%M"),
                    ),
                    NotificationType.INFO,
                )
                self.temp_array = []
                self.time_array = []
                self.temp_array.append(
                    self.get_sensor_value(self.props.get("Sensor", None)).get("value")
                )
                self.time_array.append(time.time())
                await self.push_update()

            if current_temp <= self.target_temp and self.timer.is_running is not True:
                self.timer.start()
                self.timer.is_running = True

            self.count += 1
            await asyncio.sleep(1)

        return StepResult.DONE


def setup(cbpi):
    """
    This method is called by the server during startup
    Here you need to register your plugins at the server

    :param cbpi: the cbpi core
    :return:
    """

    cbpi.plugin.register("MashInStep", MashInStep)
    cbpi.plugin.register("MashStep", MashStep)
    cbpi.plugin.register("BoilStep", BoilStep)
    cbpi.plugin.register("CooldownStep", CooldownStep)
    cbpi.plugin.register("WaitStep", WaitStep)
    cbpi.plugin.register("ToggleStep", ToggleStep)
    cbpi.plugin.register("ActorStep", ActorStep)
    cbpi.plugin.register("NotificationStep", NotificationStep)
