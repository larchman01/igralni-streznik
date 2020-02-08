import logging
from typing import Dict

from sledilnik.classes.Field import Field
from sledilnik.classes.MovableObject import MovableObject
from sledilnik.classes.TrackerLiveData import TrackerLiveData

from so2.entities.ConfigMap import ConfigMap
from so2.entities.Hive import Hive
from so2.enums.HiveTypeEnum import HiveType


class StateLiveData:
    def __init__(self):
        self.logger = logging.getLogger('sledenje-objektom.StateLiveData')
        self.robots: Dict[int, MovableObject] = {}
        self.hives: Dict[int, Hive] = {}
        self.fields: Dict[str, Field] = {}
        self.zones: Dict[str, Field] = {}
        self.config: ConfigMap = ConfigMap()

    def parseTrackerLiveData(self, data: TrackerLiveData):
        self.fields = data.fields
        self.sortMovableObjects(data.objects)

    def sortMovableObjects(self, objects: Dict[int, MovableObject]):
        for key, obj in objects.items():
            if key in self.config.healthyHives:
                self.hives[key] = Hive(obj, HiveType.HIVE_HEALTHY)
            elif key in self.config.diseasedHives:
                self.hives[key] = Hive(obj, HiveType.HIVE_DISEASED)
            else:
                self.robots[key] = obj
