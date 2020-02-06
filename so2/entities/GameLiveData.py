import json
import logging
import os
import pickle
from typing import Dict, List

from sledilnik.classes.Field import Field
from sledilnik.classes.MovableObject import MovableObject
from sledilnik.classes.TrackerLiveData import TrackerLiveData

from so2.entities.ConfigMap import ConfigMap
from so2.entities.Hive import Hive
from so2.entities.Team import Team
from so2.enums.FieldsNamesEnum import FieldsNames
from so2.enums.HiveTypeEnum import HiveType


class GameLiveData:
    def __init__(self):
        self.logger = logging.getLogger('sledenje-objektom.GameLiveData')
        self.hives: Dict[int, Hive] = {}
        self.robots: Dict[int, MovableObject] = {}
        self.teams: List[Team] = []
        self.gameOn: bool = False
        self.timeLeft: int = 0
        self.fields: Dict[int, Field] = {}
        self.zones: Dict[str, Field] = {}
        self.map: ConfigMap = self.readMap()
        self.readConfig()

    def parseTrackerLiveData(self, data: TrackerLiveData):
        self.fields = data.fields
        self.sortMovableObjects(data.objects)

    def readMap(self):
        if os.path.isfile('map.json'):
            with open('map.json') as json_file:
                return json.load(json_file)
        else:
            self.logger.critical("Can't load map.json!")
            quit(-1)

    def readConfig(self):
        self.teams.append(Team(self.map.team1RobotId, self.map.teams[self.map.team1RobotId]))
        self.teams.append(Team(self.map.team2RobotId, self.map.teams[self.map.team2RobotId]))

    def sortMovableObjects(self, objects: Dict[int, MovableObject]):
        for key, obj in objects.items():
            if key == self.map.team1RobotId:
                self.robots[key] = obj
            elif key == self.map.team2RobotId:
                self.robots[key] = obj
            elif key in self.map.healthyHives:
                self.hives[key] = Hive(obj, HiveType.HIVE_HEALTHY)
            elif key in self.map.diseasedHives:
                self.hives[key] = Hive(obj, HiveType.HIVE_DISEASED)

    def reprJSON(self):
        return {
            "objects": {
                "hives": {str(hiveId): hive.reprJSON() for hiveId, hive in self.hives.items()},
                "robots": {str(robotId): robot for robotId, robot in self.robots.items()}
            },
            "fields": {
                "baskets": {
                    "team1": self.fields[FieldsNames.TEAM1_BASKET.value],
                    "team2": self.fields[FieldsNames.TEAM2_BASKET.value]
                },
                "zones": {
                    "team1": self.fields[FieldsNames.TEAM1_ZONE.value],
                    "team2": self.fields[FieldsNames.TEAM2_ZONE.value],
                    "neutral": self.fields[FieldsNames.NEUTRAL_ZONE.value]
                },
                "battleground": self.fields[FieldsNames.BATTLEGROUND.value]
            },
            "teams": {
                "team1": self.teams[0].reprJSON(),
                "team2": self.teams[1].reprJSON()
            },
            "timeLeft": self.timeLeft,
            "gameOn": self.gameOn
        }
