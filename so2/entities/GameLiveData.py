import os
import pickle
from typing import Dict

from sledilnik.classes.Field import Field
from sledilnik.classes.MovableObject import MovableObject

from so2.entities.ConfigMap import ConfigMap
from so2.entities.Hive import Hive
from so2.entities.Team import Team
from so2.enums.FieldsNamesEnum import FieldsNames
from so2.enums.HiveTypeEnum import HiveType


class GameLiveData:
    def __init__(self):
        self.hives: Dict[int, Hive] = {}
        self.robots: Dict[int, MovableObject] = {}
        self.teams: Dict[int, Team] = {}
        self.gameOn: bool = False
        self.timeLeft: int = 0
        self.fields: Dict[int, Field] = {}
        self.zones: Dict[str, Field] = {}
        self.map: ConfigMap = self.readMap()

    @staticmethod
    def readMap():
        if os.path.isfile('map.json'):
            return pickle.load(open('map.json'))

    def setHives(self, objects: Dict[int, MovableObject]):
        for key, obj in objects.items():
            if key in self.map.healthyHives:
                self.hives[key] = Hive(obj, HiveType.HIVE_HEALTHY)
            elif key in self.map.diseasedHives:
                self.hives[key] = Hive(obj, HiveType.HIVE_DISEASED)

    def reprJSON(self):
        return {
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
            }
        }
