import asyncio
import base64
import json
import logging
import math
import os
import os.path
import pathlib
import re
import sqlite3
import webbrowser
import xml.etree.ElementTree
from os import listdir
from os.path import isfile, join

import aiohttp
import yaml
from aiohttp import web
from cbpi.api import *
from cbpi.api.base import CBPiBase
from cbpi.api.config import ConfigType
from cbpi.api.dataclasses import (Actor, Kettle, NotificationAction,
                                  NotificationType, Sensor)
from cbpi.controller.kettle_controller import KettleController
from voluptuous.schema_builder import message

from ..api.step import StepMove, StepResult, StepState


class UploadController:

    def __init__(self, cbpi):
        self.cbpi = cbpi
        self.logger = logging.getLogger(__name__)

    async def get_kbh_recipes(self):
        try:
            path = self.cbpi.config_folder.get_upload_file("kbh.db")
            conn = sqlite3.connect(path)
            c = conn.cursor()
            c.execute("SELECT ID, Sudname, Status FROM Sud")
            data = c.fetchall()
            result = []
            for row in data:
                element = {"value": str(row[0]), "label": str(row[1])}
                result.append(element)
            return result
        except:
            return []

    async def get_xml_recipes(self):
        try:
            path = self.cbpi.config_folder.get_upload_file("beer.xml")
            e = xml.etree.ElementTree.parse(path).getroot()
            result = []
            counter = 1
            for idx, val in enumerate(e.findall("RECIPE")):
                element = {"value": str(counter), "label": val.find("NAME").text}
                result.append(element)
                counter += 1
            return result
        except:
            return []

    async def get_json_recipes(self):
        try:
            path = self.cbpi.config_folder.get_upload_file("mmum.json")
            e = json.load(open(path))
            result = []
            result.append({"value": str(1), "label": e["Name"]})
            return result
        except:
            return []

    async def get_brewfather_recipes(self, offset=0):
        limit = 50
        length = self.cbpi.config.get("brewfather_list_length", 50)
        repeat = True
        brewfather = True
        result = []
        self.url = "https://api.brewfather.app/v2/recipes"
        brewfather_user_id = self.cbpi.config.get("brewfather_user_id", None)
        if brewfather_user_id == "" or brewfather_user_id is None:
            brewfather = False

        brewfather_api_key = self.cbpi.config.get("brewfather_api_key", None)
        if brewfather_api_key == "" or brewfather_api_key is None:
            brewfather = False

        if brewfather == True:
            encodedData = base64.b64encode(
                bytes(f"{brewfather_user_id}:{brewfather_api_key}", "ISO-8859-1")
            ).decode("ascii")
            headers = {"Authorization": "Basic %s" % encodedData}
            parameters = {"limit": limit}
            while repeat == True:
                try:
                    async with aiohttp.ClientSession(headers=headers) as bf_session:
                        async with bf_session.get(self.url, params=parameters) as r:
                            if r.status == 429:
                                try:
                                    seconds = int(r.headers["Retry-After"])
                                    minutes = round(seconds / 60)
                                except:
                                    seconds = None
                                if not seconds:
                                    logging.error(
                                        "Too many requests to BF api. Try again later"
                                    )
                                    self.cbpi.notify(
                                        "Error",
                                        "Too many requests to BF api. Try again later",
                                        NotificationType.ERROR,
                                    )
                                else:
                                    logging.error(
                                        f"Too many requests to BF api. Try in {minutes} minutes again."
                                    )
                                    self.cbpi.notify(
                                        "Error",
                                        f"Too many requests to BF api. Try in {minutes} minutes again.",
                                        NotificationType.ERROR,
                                    )
                                repeat = False
                                logging.error(r.headers["Retry-After"])
                            else:
                                bf_recipe_list = await r.json()
                        await bf_session.close()
                except Exception as e:
                    logging.error(e)
                    repeat = False
                try:
                    if bf_recipe_list:
                        for row in bf_recipe_list:
                            recipe_id = row["_id"]
                            name = row["name"]
                            element = {"value": recipe_id, "label": name}
                            result.append(element)
                    else:
                        repeat = False
                except Exception as e:
                    logging.error(e)
                try:
                    if len(bf_recipe_list) != limit:
                        repeat = False
                    else:
                        parameters = {"limit": limit, "start_after": recipe_id}
                except Exception as e:
                    logging.error(e)

        try:
            newlist = sorted(result, key=lambda d: d["label"])
            listlength = len(newlist)
            max = math.floor(listlength / length)
            sortlist = []
            for i in range(0, max + 1):
                sortlist.append({"value": i * length, "label": i * length})
            return newlist, sortlist, length
        except:
            logging.error("Return empty BF recipe list")
            sortlist = [{"value": 0, "label": "0"}]
            return result, sortlist, length

    def get_creation_path(self):
        creation_path = self.cbpi.config.get("RECIPE_CREATION_PATH", "upload")
        path = {"path": "upload"} if creation_path == "" else {"path": creation_path}
        return path

    def allowed_file(self, filename, extension):
        return "." in filename and filename.rsplit(".", 1)[1] in set([extension])

    async def FileUpload(self, data):
        fileData = data["File"]
        filename = fileData.filename
        recipe_file = fileData.file
        content_type = fileData.content_type

        if content_type == "text/xml":
            try:
                beer_xml = recipe_file.read().decode("utf-8", "replace")
                if recipe_file and self.allowed_file(filename, "xml"):
                    self.path = self.cbpi.config_folder.get_upload_file("beer.xml")

                    f = open(self.path, "w")
                    f.write(beer_xml)
                    f.close()
                    self.cbpi.notify(
                        "Success",
                        "XML Recipe {} has been uploaded".format(filename),
                        NotificationType.SUCCESS,
                    )
            except Exception as e:
                self.cbpi.notify(
                    "Error",
                    "XML Recipe upload failed: {}".format(e),
                    NotificationType.ERROR,
                )
                pass

        elif content_type == "application/json":
            try:
                mmum_json = recipe_file.read().decode("utf-8", "replace")
                if recipe_file and self.allowed_file(filename, "json"):
                    self.path = self.cbpi.config_folder.get_upload_file("mmum.json")

                    f = open(self.path, "w")
                    f.write(mmum_json)
                    f.close()
                    self.cbpi.notify(
                        "Success",
                        "JSON Recipe {} has been uploaded".format(filename),
                        NotificationType.SUCCESS,
                    )
            except Exception as e:
                self.cbpi.notify(
                    "Error" "JSON Recipe upload failed: {}".format(e),
                    NotificationType.ERROR,
                )
                pass

        elif content_type == "application/octet-stream":
            try:
                content = recipe_file.read()
                if recipe_file and self.allowed_file(filename, "sqlite"):
                    self.path = self.cbpi.config_folder.get_upload_file("kbh.db")

                    f = open(self.path, "wb")
                    f.write(content)
                    f.close()
                    self.cbpi.notify(
                        "Success",
                        "Kleiner Brauhelfer database has been uploaded",
                        NotificationType.SUCCESS,
                    )

            except:
                self.cbpi.notify(
                    "Error",
                    "Kleiner Brauhelfer database upload failed",
                    NotificationType.ERROR,
                )
                pass
        else:
            self.cbpi.notify(
                "Error", "Wrong content type. Upload failed", NotificationType.ERROR
            )

    # function to create a recipe from the Kleiner Brauhelfer database
    async def kbh_recipe_creation(self, Recipe_ID):
        config = self.get_config_values()
        if self.kettle is not None:
            # check if kbh database is available in the upload folder and connect to it
            self.path = self.cbpi.config_folder.get_upload_file("kbh.db")
            if os.path.exists(self.path) is False:
                self.cbpi.notify(
                    "File Not Found",
                    "Please upload a kbh V2 database file",
                    NotificationType.ERROR,
                )

            try:
                # Get Recipe Nmae
                conn = sqlite3.connect(self.path)
                c = conn.cursor()
                c.execute("SELECT Sudname FROM Sud WHERE ID = ?", (Recipe_ID,))
                row = c.fetchone()
                name = row[0]
                # get MashIn Temp
                mashin_temp = None
                c.execute(
                    "SELECT TempWasser FROM Maischplan WHERE Typ = 0 AND SudID = ?",
                    (Recipe_ID,),
                )
                row = c.fetchone()
                try:
                    if self.cbpi.config.get("TEMP_UNIT", "C") == "C":
                        mashin_temp = str(int(row[0]))
                    else:
                        mashin_temp = str(round(9.0 / 5.0 * int(row[0]) + 32))
                except:
                    pass
                # get the hop addition times
                c.execute(
                    "SELECT Zeit, Name, Vorderwuerze FROM Hopfengaben WHERE Vorderwuerze <> 1 AND SudID = ?",
                    (Recipe_ID,),
                )
                hops = c.fetchall()
                whirlpool = []
                #for hop in hops:
                #    if hop[2] == 5: # whirlpool hops are defined with Vorderwuerze = 5 in the KBH database (Ausschlagen)
                #        whirlpool.append(hop)
                #for whirl in whirlpool:
                #    hops.remove(whirl)
                # get the misc addition times
                
                c.execute(
                    "SELECT Zugabedauer, Name FROM WeitereZutatenGaben WHERE Zeitpunkt = 1 AND SudID = ?",
                    (Recipe_ID,),
                )
                miscs = c.fetchall()
                try:
                    c.execute(
                        "SELECT Zeit, Name FROM Hopfengaben WHERE Vorderwuerze = 1 AND SudID = ?",
                        (Recipe_ID,),
                    )
                    FW_Hops = c.fetchall()
                    FirstWort = self.getFirstWort(FW_Hops, "kbh")
                except:
                    FirstWort = "No"

                # get the boiltime from the database
                c.execute("SELECT Kochdauer FROM Sud WHERE ID = ?", (Recipe_ID,))
                row = c.fetchone()
                BoilTime = str(int(row[0]))

                await self.create_recipe(name)

                # create a mashin step if mashin_temp is available (just heating up to temp and waiting for user input)
                if mashin_temp is not None:
                    step_type = self.mashin if self.mashin != "" else "MashInStep"
                    step_string = {
                        "name": "MashIn",
                        "props": {
                            "AutoMode": self.AutoMode,
                            "Kettle": self.id,
                            "Sensor": self.kettle.sensor,
                            "Temp": mashin_temp,
                            "Timer": "0",
                            "Notification": "Target temperature reached. Please add malt.",
                        },
                        "status_text": "",
                        "status": "I",
                        "type": step_type,
                    }
                    await self.create_step(step_string)

                # if mashin_temp is not available, create a mashin step with the temp of the first mash step if addmashin is set to yes
                step_temp_old = 0
                for row in c.execute(
                    "SELECT Name, TempRast, DauerRast FROM Maischplan WHERE Typ <> 0 AND SudID = ?",
                    (Recipe_ID,),
                ):
                    step_temp = (float(row[1]))
                    if mashin_temp is None and self.addmashin == "Yes":
                        step_type = self.mashin if self.mashin != "" else "MashInStep"
                        step_string = {
                            "name": "MashIn",
                            "props": {
                                "AutoMode": self.AutoMode,
                                "Kettle": self.id,
                                "Sensor": self.kettle.sensor,
                                "Temp": (
                                    str(step_temp)
                                    if self.TEMP_UNIT == "C"
                                    else str(round(9.0 / 5.0 * step_temp + 32,1))
                                ),
                                "Timer": "0",
                                "Notification": "Target temperature reached. Please add malt.",
                            },
                            "status_text": "",
                            "status": "I",
                            "type": step_type,
                        }
                        await self.create_step(step_string)
                    
                    try:
                        if float(step_temp) < float(step_temp_old):
                            step_string = {
                                "name": "Temp reduction!",
                                "props": {
                                    "AutoNext": "No",
                                    "Kettle": self.id,
                                    "Notification": f"Temperature reduction from {step_temp_old}  {self.TEMP_UNIT} to {step_temp} {self.TEMP_UNIT}. Please reduce the temperature manually.",
                                },
                                "status_text": "",
                                "status": "I",
                                "type": "NotificationStep",
                            }

                            await self.create_step(step_string)
                    except Exception as e:
                        logging.error(e)


                    # create the mash steps based on the recipe settings (time and temp)
                    step_type = self.mash if self.mash != "" else "MashStep"
                    step_string = {
                        "name": str(row[0]),
                        "props": {
                            "AutoMode": self.AutoMode,
                            "Kettle": self.id,
                            "Sensor": self.kettle.sensor,
                            "Temp": (
                                str(int(row[1]))
                                if self.TEMP_UNIT == "C"
                                else str(round(9.0 / 5.0 * int(row[1]) + 32))
                            ),
                            "Timer": str(int(row[2])),
                        },
                        "status_text": "",
                        "status": "I",
                        "type": step_type,
                    }
                    await self.create_step(step_string)
                    step_temp_old = step_temp

                # MashOut -> Notification step that sends notification and waits for user input to move to next step (AutoNext=No)
                if self.mashout == "NotificationStep":
                    step_string = {
                        "name": "Lautering",
                        "props": {
                            "AutoNext": "No",
                            "Kettle": self.id,
                            "Notification": "Mash Process completed. Please start lautering and press next to start boil.",
                        },
                        "status_text": "",
                        "status": "I",
                        "type": self.mashout,
                    }
                    await self.create_step(step_string)

                # create a boil step with hop alarms and alarm for first wort hops
                Hops , Whirlpool= self.getBoilAlerts(hops, miscs, "kbh")
                step_type = self.boil if self.boil != "" else "BoilStep"
                step_string = {
                    "name": "Boil Step",
                    "props": {
                        "AutoMode": self.AutoMode,
                        "Kettle": self.boilid,
                        "Sensor": self.boilkettle.sensor,
                        "Temp": int(self.BoilTemp),
                        "Timer": BoilTime,
                        "First_Wort": FirstWort[0],
                        "First_Wort_text": FirstWort[1],
                        "LidAlert": "Yes",
                        "Hop_1": Hops[0][0],
                        "Hop_1_text": Hops[0][1],
                        "Hop_2": Hops[1][0],
                        "Hop_2_text": Hops[1][1],
                        "Hop_3": Hops[2][0],
                        "Hop_3_text": Hops[2][1],
                        "Hop_4": Hops[3][0],
                        "Hop_4_text": Hops[3][1],
                        "Hop_5": Hops[4][0],
                        "Hop_5_text": Hops[4][1],
                        "Hop_6": Hops[5][0],
                        "Hop_6_text": Hops[5][1],
                    },
                    "status_text": "",
                    "status": "I",
                    "type": step_type,
                }

                await self.create_step(step_string)

                # whirlpool hops are added at the end of the boil step
                # and the kettle is cooled down to the whirlpool temperature
                # the whirlpool temperature is set in the recipe and is used to cool down the kettle
                
                if Whirlpool != []:
 
                    step_type = self.cooldown
                    step_name = "CoolDown for Whirlpool Hop"
                    cooldown_sensor = ""
                    step_temp = float(Whirlpool)
                    step_timer = ""

                    if step_type.find("Cooldown") != -1 and self.cooldown != "":
                        cooldown_sensor = (
                                self.boilkettle.sensor
                            )  # fall back to boilkettle sensor if no other sensor is specified
                        step_string = {
                            "name": "Cooldown for Whirlpool Hop",
                            "props": {
                                "Kettle": self.boilid,
                                "Timer": step_timer,
                                "Temp": step_temp,
                                "Sensor": cooldown_sensor,
                                "Actor": self.CoolDownActor,
                            },
                            "status_text": "",
                            "status": "I",
                            "type": step_type,
                        }
                        await self.create_step(step_string)

                    if self.cooldown.find("Cooldown") != -1:
                        notification = "Target Whirlpool temperature reached. Please add Whirlpool hops." 
                        autonext = "No"
                    else: 
                        notification= f"Cool down to {step_temp} {self.TEMP_UNIT}. Then add Whirlpool hops."
                        autonext = "No"
                    step_string = {
                        "name": "Whirlpool Hop",
                        "props": {
                            "AutoNext": autonext,
                            "Kettle": self.id,
                            "Notification": notification,
                        },
                        "status_text": "",
                        "status": "I",
                        "type": "NotificationStep",
                    }
                    await self.create_step(step_string)

                # create a whirlpool step with optional cooldown
                if not whirlpool:
                    await self.create_Whirlpool_Cooldown()
                else:
                    await self.create_Whirlpool_Cooldown(
                        str(abs(whirlpool[0][0]))
                    )  # from kbh this value comes as negative but must be positive

                self.cbpi.notify("KBH Recipe created", name, NotificationType.INFO)

            except Exception as e:
                self.cbpi.notify(
                    "KBH Recipe creation failure: {}".format(e),
                    name,
                    NotificationType.ERROR,
                )
                pass
        else:
            self.cbpi.notify(
                "Recipe Upload",
                "No default Kettle defined. Please specify default Kettle in settings",
                NotificationType.ERROR,
            )

    def getJsonMashin(self, id):
        self.path = self.cbpi.config_folder.get_upload_file("mmum.json")
        e = json.load(open(self.path))
        return float(e["Einmaischtemperatur"])

    # function to create a recipe from a MUMM json recipe file
    async def json_recipe_creation(self, Recipe_ID):
        config = self.get_config_values()
        try:
            if self.kettle is not None:
                # check if  mmum-json file is located in upload folder and load it
                self.path = self.cbpi.config_folder.get_upload_file("mmum.json")
                if os.path.exists(self.path) is False:
                    self.cbpi.notify(
                        "File Not Found",
                        "Please upload a MMuM-JSON File",
                        NotificationType.ERROR,
                    )

                e = json.load(open(self.path))
                logging.info(json.dumps(e, indent=4))
                name = e["Name"]
                boil_time = float(e["Kochzeit_Wuerze"])

                logging.info(name)
                logging.info(boil_time)

                await self.create_recipe(name)

                # get the hop addition times
                hops = []
                firstHops = []
                whirlpool_hops = []

                Hopfenliste=e["Hopfenkochen"]
                for Hopfen in Hopfenliste:
                    #logging.error(Hopfen)
                    if Hopfen["Typ"] == "Standard":
                        hops.append({"name": Hopfen["Sorte"], "time": Hopfen["Zeit"]})
                    if Hopfen["Typ"] == "Vorderwuerze":
                        firstHops.append({"name": Hopfen["Sorte"]})
                    if Hopfen["Typ"] == "Whirlpool":
                        whirlpool_hops.append({"name": Hopfen["Sorte"]})
 
                #logging.error(hops)
                #logging.error(firstHops)
                #logging.error(whirlpool_hops)

                FirstWort = self.getFirstWort(firstHops, "json")
                #logging.error(FirstWort)
                miscs = []
                try:
                    weitere_zutaten=e["Gewuerze_etc"]
                    for zutat in weitere_zutaten:
                        miscs.append({"name": zutat["Name"], "time": zutat["Kochzeit"]})
                #logging.error(miscs)
                except:
                    pass
                # Mash Steps -> first step is different as it heats up to defined temp and stops with notification to add malt
                # AutoMode is yes to start and stop automatic mode or each step
                MashIn_Flag = True
                step_kettle = self.id
                last_step_temp = 0
                step_temp_old = 0
                logging.info(
                    step_kettle
                )  ###################################################
                for row in self.getSteps(Recipe_ID, "json"):
                    step_name = str(row.get("name"))
                    step_timer = str(int(row.get("timer")))
                    step_temp = str(int(row.get("temp")))
                    last_step_temp = step_temp
                    sensor = self.kettle.sensor
                    if MashIn_Flag == True:
                        if row.get("timer") == 0:
                            step_type = (
                                self.mashin if self.mashin != "" else "MashInStep"
                            )
                            Notification = (
                                "Target temperature reached. Please add malt."
                            )
                            MashIn_Flag = False
                            if step_name is None or step_name == "":
                                step_name = "MashIn"
                        elif self.addmashin == "Yes":
                            step_type = (
                                self.mashin if self.mashin != "" else "MashInStep"
                            )
                            Notification = (
                                "Target temperature reached. Please add malt."
                            )
                            MashIn_Flag = False
                            step_string = {
                                "name": "MashIn",
                                "props": {
                                    "AutoMode": self.AutoMode,
                                    "Kettle": self.id,
                                    "Sensor": self.kettle.sensor,
                                    "Temp": self.getJsonMashin(Recipe_ID),
                                    "Timer": 0,
                                    "Notification": Notification,
                                },
                                "status_text": "",
                                "status": "I",
                                "type": step_type,
                            }
                            await self.create_step(step_string)
                            logging.info(
                                step_kettle
                            )  ###################################################

                            step_type = self.mash if self.mash != "" else "MashStep"
                            Notification = ""
                        else:
                            step_type = self.mash if self.mash != "" else "MashStep"
                            Notification = ""

                    else:
                        step_type = self.mash if self.mash != "" else "MashStep"
                        Notification = ""

                    try:
                        if float(step_temp) < float(step_temp_old):
                            step_string = {
                                "name": "Temp reduction!",
                                "props": {
                                    "AutoNext": "No",
                                    "Kettle": self.id,
                                    "Notification": f"Temperature reduction from {step_temp_old}  {self.TEMP_UNIT} to {step_temp} {self.TEMP_UNIT}. Please reduce the temperature manually.",
                                },
                                "status_text": "",
                                "status": "I",
                                "type": "NotificationStep",
                            }

                            await self.create_step(step_string)
                    except Exception as e:
                        logging.error(e)

                    step_string = {
                        "name": step_name,
                        "props": {
                            "AutoMode": self.AutoMode,
                            "Kettle": self.id,
                            "Sensor": self.kettle.sensor,
                            "Temp": step_temp,
                            "Timer": step_timer,
                            "Notification": Notification,
                        },
                        "status_text": "",
                        "status": "I",
                        "type": step_type,
                    }

                    await self.create_step(step_string)
                    step_temp_old = step_temp
                # MashOut -> mashStep to reach mashout-temp for 1 min
                if last_step_temp != e["Abmaischtemperatur"]:
                    step_string = {
                        "name": "MashOut",
                        "props": {
                            "AutoMode": self.AutoMode,
                            "Kettle": self.id,
                            "Sensor": self.kettle.sensor,
                            "Temp": e["Abmaischtemperatur"],
                            "Timer": 1,
                            "Notification": "",
                        },
                        "status_text": "",
                        "status": "I",
                        "type": "MashStep",
                    }

                    await self.create_step(step_string)
                # Lautering -> Simple step that sends notification and waits for user input to move to next step (AutoNext=No)
                if self.mashout == "NotificationStep":
                    step_string = {
                        "name": "Lautering",
                        "props": {
                            "AutoNext": "No",
                            "Kettle": self.id,
                            "Notification": "Mash Process completed. Please start lautering and press next to start boil.",
                        },
                        "status_text": "",
                        "status": "I",
                        "type": self.mashout,
                    }
                    await self.create_step(step_string)

                # Measure Original Gravity -> Simple step that sends notification
                step_string = {
                    "name": "Measure Original Gravity",
                    "props": {
                        "AutoNext": "No",
                        "Kettle": self.id,
                        "Notification": "What is the original gravity of the beer wort?",
                    },
                    "status_text": "",
                    "status": "I",
                    "type": "NotificationStep",
                }
                await self.create_step(step_string)

                # Boil step including hop alarms and alarm for first wort hops -> Automode is set tu yes
                Hops, Whirlpool = self.getBoilAlerts(hops, miscs, "json")
                step_kettle = self.boilid
                step_type = self.boil if self.boil != "" else "BoilStep"
                step_time = str(int(boil_time))
                step_temp = self.BoilTemp
                sensor = self.boilkettle.sensor
                LidAlert = "Yes"

                logging.info(
                    step_temp
                )  ###################################################

                step_string = {
                    "name": "Boil Step",
                    "props": {
                        "AutoMode": self.AutoMode,
                        "Kettle": step_kettle,
                        "Sensor": sensor,
                        "Temp": step_temp,
                        "Timer": step_time,
                        "First_Wort": FirstWort[0],
                        "First_Wort_text": FirstWort[1],
                        "LidAlert": LidAlert,
                        "Hop_1": Hops[0][0],
                        "Hop_1_text": Hops[0][1],
                        "Hop_2": Hops[1][0],
                        "Hop_2_text": Hops[1][1],
                        "Hop_3": Hops[2][0],
                        "Hop_3_text": Hops[2][1],
                        "Hop_4": Hops[3][0],
                        "Hop_4_text": Hops[3][1],
                        "Hop_5": Hops[4][0],
                        "Hop_5_text": Hops[4][1],
                        "Hop_6": Hops[5][0],
                        "Hop_6_text": Hops[5][1],
                    },
                    "status_text": "",
                    "status": "I",
                    "type": step_type,
                }

                await self.create_step(step_string)

                # Measure Original Gravity -> Simple step that sends notification
                step_string = {
                    "name": "Measure Original Gravity",
                    "props": {
                        "AutoNext": "No",
                        "Kettle": self.id,
                        "Notification": "What is the original gravity of the beer wort?",
                    },
                    "status_text": "",
                    "status": "I",
                    "type": "NotificationStep",
                }
                await self.create_step(step_string)

                                # whirlpool hops are added at the end of the boil step
                # and the kettle is cooled down to the whirlpool temperature
                # the whirlpool temperature is set in the recipe and is used to cool down the kettle
                
                if whirlpool_hops != []:

                    step_temp = 80 if self.TEMP_UNIT == "C" else 176

                    step_type = self.cooldown
                    step_name = "CoolDown for Whirlpool Hop"
                    cooldown_sensor = ""
                    step_timer = ""

                    if step_type.find("Cooldown") != -1 and self.cooldown != "":
                        cooldown_sensor = (
                                self.boilkettle.sensor
                            )  # fall back to boilkettle sensor if no other sensor is specified
                        step_string = {
                            "name": "Cooldown for Whirlpool Hop",
                            "props": {
                                "Kettle": self.boilid,
                                "Timer": step_timer,
                                "Temp": step_temp,
                                "Sensor": cooldown_sensor,
                                "Actor": self.CoolDownActor,
                            },
                            "status_text": "",
                            "status": "I",
                            "type": step_type,
                        }
                        await self.create_step(step_string)

                    if self.cooldown.find("Cooldown") != -1:
                        notification = "Target Whirlpool temperature reached. Please add Whirlpool hops." 
                        autonext = "No"
                    else: 
                        notification= f"Cool down to {step_temp} {self.TEMP_UNIT}. Then add Whirlpool hops."
                        autonext = "No"
                    step_string = {
                        "name": "Whirlpool Hop",
                        "props": {
                            "AutoNext": autonext,
                            "Kettle": self.id,
                            "Notification": notification,
                        },
                        "status_text": "",
                        "status": "I",
                        "type": "NotificationStep",
                    }
                    await self.create_step(step_string)



                await self.create_Whirlpool_Cooldown()

                self.cbpi.notify(
                    "MMuM-JSON Recipe created ", name, NotificationType.INFO
                )
            else:
                self.cbpi.notify(
                    "Recipe Upload",
                    "No default Kettle defined. Please specify default Kettle in settings",
                    NotificationType.ERROR,
                )
        except Exception as e:
            self.cbpi.notify(
                "MMuM-JSON Recipe creation failure: {}".format(e),
                name,
                NotificationType.ERROR,
            )
            self.logger.error(e)

    async def xml_recipe_creation(self, Recipe_ID):
        config = self.get_config_values()
        try:
            if self.kettle is not None:
                # load beerxml file located in upload folder
                self.path = self.cbpi.config_folder.get_upload_file("beer.xml")
                if os.path.exists(self.path) is False:
                    self.cbpi.notify(
                        "File Not Found",
                        "Please upload a Beer.xml File",
                        NotificationType.ERROR,
                    )

                e = xml.etree.ElementTree.parse(self.path).getroot()
                recipe = e.find("./RECIPE[%s]" % (str(Recipe_ID)))
                hops = recipe.findall("./HOPS/HOP")
                miscs = recipe.findall('MISCS/MISC[USE="Boil"]')
                name = e.find("./RECIPE[%s]/NAME" % (str(Recipe_ID))).text
                boil_time = float(
                    e.find("./RECIPE[%s]/BOIL_TIME" % (str(Recipe_ID))).text
                )
                FirstWort = self.getFirstWort(hops, "xml")

                await self.create_recipe(name)
                # Mash Steps -> first step is different as it heats up to defined temp and stops with notification to add malt
                # AutoMode is yes to start and stop automatic mode or each step
                MashIn_Flag = True
                step_kettle = self.id
                step_temp_old = 0
                for row in self.getSteps(Recipe_ID, "xml"):
                    step_name = str(row.get("name"))
                    step_timer = str(int(row.get("timer")))
                    step_temp = str(int(row.get("temp")))
                    sensor = self.kettle.sensor
                    if MashIn_Flag == True:
                        if row.get("timer") == 0:
                            step_type = (
                                self.mashin if self.mashin != "" else "MashInStep"
                            )
                            Notification = (
                                "Target temperature reached. Please add malt."
                            )
                            MashIn_Flag = False
                            if step_name is None or step_name == "":
                                step_name = "MashIn"
                        elif self.addmashin == "Yes":
                            step_type = (
                                self.mashin if self.mashin != "" else "MashInStep"
                            )
                            Notification = (
                                "Target temperature reached. Please add malt."
                            )
                            MashIn_Flag = False
                            step_string = {
                                "name": "MashIn",
                                "props": {
                                    "AutoMode": self.AutoMode,
                                    "Kettle": self.id,
                                    "Sensor": self.kettle.sensor,
                                    "Temp": step_temp,
                                    "Timer": 0,
                                    "Notification": Notification,
                                },
                                "status_text": "",
                                "status": "I",
                                "type": step_type,
                            }
                            await self.create_step(step_string)

                            step_type = self.mash if self.mash != "" else "MashStep"
                            Notification = ""
                        else:
                            step_type = self.mash if self.mash != "" else "MashStep"
                            Notification = ""

                    else:
                        step_type = self.mash if self.mash != "" else "MashStep"
                        Notification = ""

                    try:
                        if float(step_temp) < float(step_temp_old):
                            step_string = {
                                "name": "Temp reduction!",
                                "props": {
                                    "AutoNext": "No",
                                    "Kettle": self.id,
                                    "Notification": f"Temperature reduction from {step_temp_old}  {self.TEMP_UNIT} to {step_temp} {self.TEMP_UNIT}. Please reduce the temperature manually.",
                                },
                                "status_text": "",
                                "status": "I",
                                "type": "NotificationStep",
                            }

                            await self.create_step(step_string)
                    except Exception as e:
                        logging.error(e)

                    step_string = {
                        "name": step_name,
                        "props": {
                            "AutoMode": self.AutoMode,
                            "Kettle": self.id,
                            "Sensor": self.kettle.sensor,
                            "Temp": step_temp,
                            "Timer": step_timer,
                            "Notification": Notification,
                        },
                        "status_text": "",
                        "status": "I",
                        "type": step_type,
                    }

                    await self.create_step(step_string)
                    step_temp_old = step_temp

                # MashOut -> Simple step that sends notification and waits for user input to move to next step (AutoNext=No)
                if self.mashout == "NotificationStep":
                    step_string = {
                        "name": "Lautering",
                        "props": {
                            "AutoNext": "No",
                            "Kettle": self.id,
                            "Notification": "Mash Process completed. Please start lautering and press next to start boil.",
                        },
                        "status_text": "",
                        "status": "I",
                        "type": self.mashout,
                    }
                    await self.create_step(step_string)

                # Boil step including hop alarms and alarm for first wort hops -> Automode is set tu yes
                Hops , Whirlpool = self.getBoilAlerts(hops, miscs, "xml")
                step_kettle = self.boilid
                step_type = self.boil if self.boil != "" else "BoilStep"
                step_time = str(int(boil_time))
                step_temp = self.BoilTemp
                sensor = self.boilkettle.sensor
                LidAlert = "Yes"

                step_string = {
                    "name": "Boil Step",
                    "props": {
                        "AutoMode": self.AutoMode,
                        "Kettle": step_kettle,
                        "Sensor": sensor,
                        "Temp": step_temp,
                        "Timer": step_time,
                        "First_Wort": FirstWort[0],
                        "First_Wort_text": FirstWort[1],
                        "LidAlert": LidAlert,
                        "Hop_1": Hops[0][0],
                        "Hop_1_text": Hops[0][1],
                        "Hop_2": Hops[1][0],
                        "Hop_2_text": Hops[1][1],
                        "Hop_3": Hops[2][0],
                        "Hop_3_text": Hops[2][1],
                        "Hop_4": Hops[3][0],
                        "Hop_4_text": Hops[3][1],
                        "Hop_5": Hops[4][0],
                        "Hop_5_text": Hops[4][1],
                        "Hop_6": Hops[5][0],
                        "Hop_6_text": Hops[5][1],
                    },
                    "status_text": "",
                    "status": "I",
                    "type": step_type,
                }

                await self.create_step(step_string)

                # whirlpool hops are added at the end of the boil step
                # and the kettle is cooled down to the whirlpool temperature
                # the whirlpool temperature is set in the recipe and is used to cool down the kettle
                
                if Whirlpool != []:
                    logging.info(
                        "Whirlpool Temp: {}".format(Whirlpool)
                    )

                    step_type = self.cooldown
                    step_name = "CoolDown for Whirlpool Hop"
                    cooldown_sensor = ""
                    step_temp = float(Whirlpool)
                    step_timer = ""

                    if step_type.find("Cooldown") != -1 and self.cooldown != "":
                        cooldown_sensor = (
                                self.boilkettle.sensor
                            )  # fall back to boilkettle sensor if no other sensor is specified
                        step_string = {
                            "name": "Cooldown for Whirlpool Hop",
                            "props": {
                                "Kettle": self.boilid,
                                "Timer": step_timer,
                                "Temp": step_temp,
                                "Sensor": cooldown_sensor,
                                "Actor": self.CoolDownActor,
                            },
                            "status_text": "",
                            "status": "I",
                            "type": step_type,
                        }
                        await self.create_step(step_string)

                    if self.cooldown.find("Cooldown") != -1:
                        notification = "Target Whirlpool temperature reached. Please add Whirlpool hops." 
                        autonext = "No"
                    else: 
                        notification= f"Cool down to {step_temp} {self.TEMP_UNIT}. Then add Whirlpool hops."
                        autonext = "No"
                    step_string = {
                        "name": "Whirlpool Hop",
                        "props": {
                            "AutoNext": autonext,
                            "Kettle": self.id,
                            "Notification": notification,
                        },
                        "status_text": "",
                        "status": "I",
                        "type": "NotificationStep",
                    }
                    await self.create_step(step_string)

                await self.create_Whirlpool_Cooldown()

                self.cbpi.notify("BeerXML Recipe created ", name, NotificationType.INFO)
            else:
                self.cbpi.notify(
                    "Recipe Upload",
                    "No default Kettle defined. Please specify default Kettle in settings",
                    NotificationType.ERROR,
                )
        except Exception as e:
            self.cbpi.notify(
                "BeerXML Recipe creation failure: {}".format(e),
                name,
                NotificationType.ERROR,
            )
            logging.error(e)
            pass

    # XML functions to retrieve xml repice parameters (if multiple recipes are stored in one xml file, id could be used)
    def getSteps(self, id, recipe_type):
        steps = []
        if recipe_type == "xml":
            e = xml.etree.ElementTree.parse(self.path).getroot()
            for e in e.findall("./RECIPE[%s]/MASH/MASH_STEPS/MASH_STEP" % (str(id))):
                if self.cbpi.config.get("TEMP_UNIT", "C") == "C":
                    temp = float(e.find("STEP_TEMP").text)
                else:
                    temp = round(9.0 / 5.0 * float(e.find("STEP_TEMP").text) + 32, 2)
                steps.append(
                    {
                        "name": e.find("NAME").text,
                        "temp": temp,
                        "timer": float(e.find("STEP_TIME").text),
                    }
                )
        elif recipe_type == "json":
            self.path = self.cbpi.config_folder.get_upload_file("mmum.json")
            e = json.load(open(self.path))
            Rasten= e["Rasten"]
            idx = 1
            for Rast in Rasten:
                if self.cbpi.config.get("TEMP_UNIT", "C") == "C":
                    temp = float(Rast["Temperatur"])
                else:
                    temp = round(
                        9.0 / 5.0 * float(Rast["Temperatur"])
                        + 32,
                        2,
                    )

                time= float(Rast["Zeit"])
                steps.append(
                    {
                        "name": "Rast {}".format(idx),
                        "temp": temp,
                        "timer": time,
                    }
                )
                idx += 1
            logging.info(steps)
        return steps

    async def bf_recipe_creation(self, Recipe_ID):
        config = self.get_config_values()

        if self.kettle is not None:

            brewfather = True
            result = []
            self.bf_url = "https://api.brewfather.app/v2/recipes/" + Recipe_ID
            brewfather_user_id = self.cbpi.config.get("brewfather_user_id", None)
            if brewfather_user_id == "" or brewfather_user_id is None:
                brewfather = False

            brewfather_api_key = self.cbpi.config.get("brewfather_api_key", None)
            if brewfather_api_key == "" or brewfather_api_key is None:
                brewfather = False

            if brewfather == True:
                encodedData = base64.b64encode(
                    bytes(f"{brewfather_user_id}:{brewfather_api_key}", "ISO-8859-1")
                ).decode("ascii")
                headers = {"Authorization": "Basic %s" % encodedData}
                bf_recipe = ""

                async with aiohttp.ClientSession(headers=headers) as bf_session:
                    async with bf_session.get(self.bf_url) as r:
                        bf_recipe = await r.json()
                    await bf_session.close()

            if bf_recipe != "":
                try:
                    StrikeTemp = bf_recipe["data"]["strikeTemp"]
                except:
                    StrikeTemp = None
                # BF is sending all Temeprature values in °C. If system is running in F, values need to be converted
                if StrikeTemp is not None and self.TEMP_UNIT != "C":
                    StrikeTemp = round((9.0 / 5.0 * float(StrikeTemp) + 32))

                RecipeName = bf_recipe["name"]
                BoilTime = bf_recipe["boilTime"]
                mash_steps = bf_recipe["mash"]["steps"]
                hops = bf_recipe["hops"]

                try:
                    miscs = bf_recipe["miscs"]
                except:
                    miscs = None

                try:
                    fermentation_steps = bf_recipe["fermentation"]["steps"]
                except:
                    fermentation_steps = None

                if fermentation_steps is not None:
                    try:
                        step = fermentation_steps[0]
                        self.fermentation_step_temp = int(step["stepTemp"])
                    except:
                        self.fermentation_step_temp = None

                if self.fermentation_step_temp is not None and self.TEMP_UNIT != "C":
                    self.fermentation_step_temp = round(
                        (9.0 / 5.0 * float(self.fermentation_step_temp) + 32)
                    )

                FirstWort = self.getFirstWort(hops, "bf")

                await self.create_recipe(RecipeName)

                # Mash Steps -> first step is different as it heats up to defined temp and stops with notification to add malt
                # AutoMode is yes to start and stop automatic mode or each step
                MashIn_Flag = True
                step_kettle = self.id
                step_temp_old = 0
                for step in mash_steps:
                    try:
                        step_name = step["name"]
                        if step_name == "":
                            step_name = "MashStep"
                    except:
                        step_name = "MashStep"

                    step_timer = str(int(step["stepTime"]))

                    if self.TEMP_UNIT == "C":
                        step_temp = str(int(step["stepTemp"]))
                    else:
                        step_temp = str(round((9.0 / 5.0 * int(step["stepTemp"]) + 32)))

                    sensor = self.kettle.sensor
                    if MashIn_Flag == True:

                        if int(step_timer) == 0:
                            step_type = (
                                self.mashin if self.mashin != "" else "MashInStep"
                            )
                            Notification = (
                                "Target temperature reached. Please add malt."
                            )
                            MashIn_Flag = False

                        elif self.addmashin == "Yes":
                            mashin_temp = (
                                str(round(StrikeTemp))
                                if StrikeTemp is not None
                                else step_temp
                            )
                            step_type = (
                                self.mashin if self.mashin != "" else "MashInStep"
                            )
                            Notification = (
                                "Target temperature reached. Please add malt."
                            )
                            MashIn_Flag = False
                            step_string = {
                                "name": "MashIn",
                                "props": {
                                    "AutoMode": self.AutoMode,
                                    "Kettle": self.id,
                                    "Sensor": self.kettle.sensor,
                                    "Temp": mashin_temp,
                                    "Timer": 0,
                                    "Notification": Notification,
                                },
                                "status_text": "",
                                "status": "I",
                                "type": step_type,
                            }
                            await self.create_step(step_string)

                            step_type = self.mash if self.mash != "" else "MashStep"
                            Notification = ""
                        else:
                            step_type = self.mash if self.mash != "" else "MashStep"
                            Notification = ""

                    else:
                        step_type = self.mash if self.mash != "" else "MashStep"
                        Notification = ""
                    try:
                        if float(step_temp) < float(step_temp_old):
                            step_string = {
                                "name": "Temp reduction!",
                                "props": {
                                    "AutoNext": "No",
                                    "Kettle": self.id,
                                    "Notification": f"Temperature reduction from {step_temp_old}  {self.TEMP_UNIT} to {step_temp} {self.TEMP_UNIT}. Please reduce the temperature manually.",
                                },
                                "status_text": "",
                                "status": "I",
                                "type": "NotificationStep",
                            }

                            await self.create_step(step_string)
                    except Exception as e:
                        logging.error(e)

                    step_string = {
                        "name": step_name,
                        "props": {
                            "AutoMode": self.AutoMode,
                            "Kettle": self.id,
                            "Sensor": self.kettle.sensor,
                            "Temp": step_temp,
                            "Timer": step_timer,
                            "Notification": Notification,
                        },
                        "status_text": "",
                        "status": "I",
                        "type": step_type,
                    }

                    await self.create_step(step_string)
                    step_temp_old = step_temp


                # MashOut -> Simple step that sends notification and waits for user input to move to next step (AutoNext=No)

                if self.mashout == "NotificationStep":
                    step_string = {
                        "name": "Lautering",
                        "props": {
                            "AutoNext": "No",
                            "Kettle": self.id,
                            "Notification": "Mash Process completed. Please start lautering and press next to start boil.",
                        },
                        "status_text": "",
                        "status": "I",
                        "type": self.mashout,
                    }
                await self.create_step(step_string)

                # Boil step including hop alarms and alarm for first wort hops -> Automode is set tu yes
                Hops, Whirlpool = self.getBoilAlerts(hops, miscs, "bf")

                step_kettle = self.boilid
                step_time = str(int(BoilTime))
                step_type = self.boil if self.boil != "" else "BoilStep"
                step_temp = self.BoilTemp
                sensor = self.boilkettle.sensor
                LidAlert = "Yes"

                step_string = {
                    "name": "Boil Step",
                    "props": {
                        "AutoMode": self.AutoMode,
                        "Kettle": step_kettle,
                        "Sensor": sensor,
                        "Temp": step_temp,
                        "Timer": step_time,
                        "First_Wort": FirstWort[0],
                        "First_Wort_text": FirstWort[1],
                        "LidAlert": LidAlert,
                        "Hop_1": Hops[0][0],
                        "Hop_1_text": Hops[0][1],
                        "Hop_2": Hops[1][0],
                        "Hop_2_text": Hops[1][1],
                        "Hop_3": Hops[2][0],
                        "Hop_3_text": Hops[2][1],
                        "Hop_4": Hops[3][0],
                        "Hop_4_text": Hops[3][1],
                        "Hop_5": Hops[4][0],
                        "Hop_5_text": Hops[4][1],
                        "Hop_6": Hops[5][0],
                        "Hop_6_text": Hops[5][1],
                    },
                    "status_text": "",
                    "status": "I",
                    "type": step_type,
                }

                await self.create_step(step_string)

                # whirlpool hops are added at the end of the boil step
                # and the kettle is cooled down to the whirlpool temperature
                # the whirlpool temperature is set in the recipe and is used to cool down the kettle
                
                if Whirlpool != []:
                    logging.info(
                        "Whirlpool Temp: {}".format(Whirlpool)
                    )

                    step_type = self.cooldown
                    step_name = "CoolDown for Whirlpool Hop"
                    cooldown_sensor = ""
                    step_temp = float(Whirlpool)
                    step_timer = ""

                    if step_type.find("Cooldown") != -1 and self.cooldown != "":
                        cooldown_sensor = (
                                self.boilkettle.sensor
                            )  # fall back to boilkettle sensor if no other sensor is specified
                        step_string = {
                            "name": "Cooldown for Whirlpool Hop",
                            "props": {
                                "Kettle": self.boilid,
                                "Timer": step_timer,
                                "Temp": step_temp,
                                "Sensor": cooldown_sensor,
                                "Actor": self.CoolDownActor,
                            },
                            "status_text": "",
                            "status": "I",
                            "type": step_type,
                        }
                        await self.create_step(step_string)

                    if self.cooldown.find("Cooldown") != -1:
                        notification = "Target Whirlpool temperature reached. Please add Whirlpool hops." 
                        autonext = "No"
                    else: 
                        notification= f"Cool down to {step_temp} {self.TEMP_UNIT}. Then add Whirlpool hops."
                        autonext = "No"
                    step_string = {
                        "name": "Whirlpool Hop",
                        "props": {
                            "AutoNext": autonext,
                            "Kettle": self.id,
                            "Notification": notification,
                        },
                        "status_text": "",
                        "status": "I",
                        "type": "NotificationStep",
                    }
                    await self.create_step(step_string)


                await self.create_Whirlpool_Cooldown()

                self.cbpi.notify(
                    "Brewfather App Recipe created: ", RecipeName, NotificationType.INFO
                )
        else:
            self.cbpi.notify(
                "Recipe Upload",
                "No default Kettle defined. Please specify default Kettle in settings",
                NotificationType.ERROR,
            )

    def getBoilAlerts(self, hops, miscs, recipe_type):
        alerts = []
        whirlpool = []
        for hop in hops:
            if recipe_type == "xml":
                use = hop.find("USE").text
                ## Hops which are not used in the boil step should not cause alerts
                if use == "Boil":
                    alerts.append([float(hop.find("TIME").text), hop.find("NAME").text])
                elif use == "Aroma":
                    try:
                        if self.TEMP_UNIT == "C":
                            temp = float(hop.find("TEMP").text)
                        else:
                            temp = round(9.0 / 5.0 * float(hop.find("TEMP").text) + 32, 2)
                    except:
                        temp = 80 if self.TEMP_UNIT == "C" else 176
                    whirlpool.append([temp, hop.find("NAME").text])

            elif recipe_type == "bf":
                use = hop["use"]
                if use == "Boil":
                    alerts.append([float(hop["time"]), hop["name"]])  ## TODO: Testing
                elif use == "Aroma":
                    try:
                        if self.TEMP_UNIT == "C":
                            temp = float(hop["temp"])
                        else:
                            temp = round(9.0 / 5.0 * float(hop["temp"]) + 32, 2)
                    except:
                        temp = 80 if self.TEMP_UNIT == "C" else 176
                    whirlpool.append([temp, hop["name"]])

            elif recipe_type == "kbh":
                if hop[2] != 5:
                    alerts.append([float(hop[0]), hop[1]])
                if hop[2] == 5:
                    temp = 80 if self.TEMP_UNIT == "C" else 176
                    whirlpool.append([temp, hop[1]])

            elif recipe_type == "json":
                alerts.append([float(hop["time"]), hop["name"]])



        ## There might also be miscelaneous additions during boild time
        if miscs is not None:
            for misc in miscs:
                if recipe_type == "xml":
                    alerts.append(
                        [float(misc.find("TIME").text), misc.find("NAME").text]
                    )
                elif recipe_type == "bf":
                    use = misc["use"]
                    if use != "Aroma" and use != "Boil":
                        continue
                    alerts.append([float(misc["time"]), misc["name"]])  ## TODO: Testing
                elif recipe_type == "kbh":
                    alerts.append([float(misc[0]), misc[1]])
                elif recipe_type == "json":
                    alerts.append([float(misc["time"]), misc["name"]])
        ## Dedupe and order the additions by their time
        ## CBP should have these additions in reverse
        alerts = sorted(alerts, key=lambda x: x[0], reverse=True)
        hop_alerts = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
        ]
        for i in range(0, 6):
            try:
                if float(alerts[i][0]) > -1:
                    hop_alerts[i] = alerts[i]
            except:
                pass
        whirlpool_temps = sorted(whirlpool, key=lambda x: x[0], reverse=True)
        logging.info("Whirlpool Hops: {}".format(whirlpool_temps))
        try:
            whirlpool_temp = whirlpool_temps[0][0]
        except:
            whirlpool_temp = []
        logging.info("Whirlpool Temp: {}".format(whirlpool_temp))
        return hop_alerts, whirlpool_temp

    def getFirstWort(self, hops, recipe_type):
        alert = "No"
        names = []
        if recipe_type == "kbh":
            if len(hops) != 0:
                alert = "Yes"
                for hop in hops:
                    names.append(hop[1])
        elif recipe_type == "xml":
            for hop in hops:
                use = hop.find("USE").text
                ## Hops which are not used in the boil step should not cause alerts
                if use != "First Wort":
                    continue
                alert = "Yes"
                names.append(hop.find("NAME").text)
        elif recipe_type == "bf":
            for hop in hops:
                if hop["use"] == "First Wort":
                    alert = "Yes"
                    names.append(hop["name"])  ## TODO: Testing
        elif recipe_type == "json":
            if len(hops) != 0:
                alert = "Yes"
                for hop in hops:
                    names.append(hop["name"])

        return [alert, " and ".join(names)]

    async def create_Whirlpool_Cooldown(self, time: str = "15"):
        # Add Waitstep as Whirlpool
        if self.cooldown != "WaiStep" and self.cooldown != "":
            step_string = {
                "name": "Whirlpool",
                "props": {"Kettle": self.boilid, "Timer": time},
                "status_text": "",
                "status": "I",
                "type": "WaitStep",
            }
            await self.create_step(step_string)

        # CoolDown step is sending a notification when cooldowntemp is reached
        step_type = self.cooldown if self.cooldown != "" else "WaitStep"
        step_name = "CoolDown"
        cooldown_sensor = ""
        step_temp = ""
        step_timer = time
        if step_type.find("Cooldown") != -1:
            cooldown_sensor = self.cbpi.config.get("steps_cooldown_sensor", None)
            if cooldown_sensor is None or cooldown_sensor == "":
                cooldown_sensor = (
                    self.boilkettle.sensor
                )  # fall back to boilkettle sensor if no other sensor is specified
            step_timer = ""
            try:
                step_temp = (
                    int(self.CoolDownTemp)
                    if (
                        self.fermentation_step_temp is None
                        or self.fermentation_step_temp <= int(self.CoolDownTemp)
                    )
                    else self.fermentation_step_temp
                )
            except:
                step_temp = int(self.CoolDownTemp)
            step_string = {
                "name": "Cooldown",
                "props": {
                    "Kettle": self.boilid,
                    "Timer": step_timer,
                    "Temp": step_temp,
                    "Sensor": cooldown_sensor,
                    "Actor": self.CoolDownActor,
                },
                "status_text": "",
                "status": "I",
                "type": step_type,
            }
            await self.create_step(step_string)
      
    def get_config_values(self):
        self.kettle = None
        self.boilkettle = None
        # Define MashSteps
        self.TEMP_UNIT = self.cbpi.config.get("TEMP_UNIT", "C")
        self.AutoMode = self.cbpi.config.get("AutoMode", "Yes")
        self.mashin = self.cbpi.config.get("steps_mashin", "MashInStep")
        self.mash = self.cbpi.config.get("steps_mash", "MashStep")
        self.mashout = self.cbpi.config.get(
            "steps_mashout", None
        )  # Currently used only for the Braumeister
        self.boil = self.cbpi.config.get("steps_boil", "BoilStep")
        self.whirlpool = "Waitstep"
        self.cooldown = self.cbpi.config.get("steps_cooldown", "WaitStep")
        # get default boil temp from settings
        self.BoilTemp = self.cbpi.config.get("steps_boil_temp", 98)
        # get default cooldown temp alarm setting
        self.CoolDownTemp = self.cbpi.config.get("steps_cooldown_temp", 25)
        self.CoolDownActor = self.cbpi.config.get("steps_cooldown_actor", None)
        # get default Kettle from Settings
        self.id = self.cbpi.config.get("MASH_TUN", None)
        self.boilid = self.cbpi.config.get("BoilKettle", None)
        if self.boilid is None:
            self.boilid = self.id
        # If next parameter is Yes, MashIn Ste will be added before first mash step if not included in recipe
        self.addmashin = self.cbpi.config.get("AddMashInStep", "Yes")

        try:
            self.kettle = self.cbpi.kettle.find_by_id(self.id)
        except:
            self.cbpi.notify(
                "Recipe Upload",
                "No default Kettle defined. Please specify default Kettle in settings",
                NotificationType.ERROR,
            )
        try:
            self.boilkettle = self.cbpi.kettle.find_by_id(self.boilid)
        except:
            self.boilkettle = self.kettle

        config_values = {
            "kettle": self.kettle,
            "kettle_id": str(self.id),
            "boilkettle": self.boilkettle,
            "boilkettle_id": str(self.boilid),
            "mashin": str(self.mashin),
            "mash": str(self.mash),
            "mashout": str(self.mashout),
            "boil": str(self.boil),
            "whirlpool": str(self.whirlpool),
            "cooldown": str(self.cooldown),
            "boiltemp": str(self.BoilTemp),
            "cooldowntemp": str(self.CoolDownTemp),
            "cooldownactor": self.CoolDownActor,
            "temp_unit": str(self.TEMP_UNIT),
            "AutoMode": str(self.AutoMode),
        }
        logging.info(config_values)
        return config_values

    async def create_recipe(self, name):
        # Create recipe in recipe Book with name of first recipe in xml file
        self.recipeID = await self.cbpi.recipe.create(name)
        # send recipe to mash profile
        await self.cbpi.recipe.brew(self.recipeID)
        # remove empty recipe from recipe book
        await self.cbpi.recipe.remove(self.recipeID)

    # function to create json to be send to api to add a step to the current mash profile. Currently all properties are send to each step which does not cuase an issue
    async def create_step(self, step_string):
        # get server port from settings and define url for api calls -> adding steps
        self.port = str(self.cbpi.static_config.get("port", 8000))
        self.url = "http://127.0.0.1:" + self.port + "/step2/"
        # convert step:string to json required for api call.
        step = json.dumps(step_string)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(self.url, data=step) as response:
                return await response.text()
            await self.push_update()