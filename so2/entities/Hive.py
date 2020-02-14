from typing import Dict

from sledilnik.classes.MovableObject import MovableObject

from so2.entities.ConfigMap import ConfigMap
from so2.enums.ConfigEnum import Config
from so2.enums.FieldsNamesEnum import FieldsNames
from so2.enums.HiveTypeEnum import HiveType


class Hive(MovableObject):
    def __init__(self, obj: MovableObject, hiveType: HiveType):
        super().__init__(obj.id, obj.pos.x, obj.pos.y, obj.direction)
        self.hiveType: HiveType = hiveType
        self.zones: Dict[FieldsNames, int] = {}

    def addZone(self, zone: FieldsNames):
        self.zones[zone] = 1

    def getPoints(self, team, config: ConfigMap) -> int:
        if team == Config.TEAM1:
            if FieldsNames.TEAM2_ZONE in self.zones:
                return config.points[Config.ENEMY.value]
            elif FieldsNames.NEUTRAL_ZONE in self.zones:
                return config.points[Config.NEUTRAL.value]
            else:
                return config.points[Config.HOME.value]
        elif team == Config.TEAM2:
            if FieldsNames.TEAM1_ZONE in self.zones:
                return config.points[Config.ENEMY.value]
            elif FieldsNames.NEUTRAL_ZONE in self.zones:
                return config.points[Config.NEUTRAL.value]
            else:
                return config.points[Config.HOME.value]

    def reprJSON(self):
        json = super().reprJSON()
        json["type"] = self.hiveType.value
        return json
