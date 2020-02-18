import logging
from timeit import default_timer as timer
from typing import Dict, List

from shapely.geometry import Point as SPoint
from shapely.geometry.polygon import Polygon as SPolygon
from sledilnik.classes.Field import Field
from sledilnik.classes.MovableObject import MovableObject
from sledilnik.classes.Point import Point

from so2.entities.ConfigMap import ConfigMap
from so2.entities.Hive import Hive
from so2.entities.StateLiveData import StateLiveData
from so2.entities.Team import Team
from so2.enums.ConfigEnum import Config
from so2.enums.FieldsNamesEnum import FieldsNames
from so2.enums.HiveTypeEnum import HiveType


class GameLiveData:
    def __init__(self, team1RobotId, team2RobotId):
        self.logger = logging.getLogger('sledenje-objektom.GameLiveData')
        self.gameOn: bool = False
        self.gameTime: int = 100
        self.startTime: float = timer()
        self.config = ConfigMap()

        self.robots: Dict[int, MovableObject] = {}
        self.teams: Dict[Config, Team] = {}
        self.addTeam(Config.TEAM1, team1RobotId)
        self.addTeam(Config.TEAM2, team2RobotId)
        self.time: float = timer()

        self.score: List[int] = [0, 0]
        self.alterScore: List[int] = [0, 0]

        self.hivesStartingZones: Dict[int, FieldsNames] = {}

    def addTeam(self, team: Config, robotId):
        if str(robotId) in self.config.teams:
            self.teams[team] = Team(robotId, self.config.teams[str(robotId)])
        else:
            logging.error("Team with specified id does not exist in config!")

    def startGame(self):
        self.score = [0, 0]
        self.gameOn = True
        self.startTime = timer()
        self.hivesStartingZones = {}

    def checkHiveZones(self, stateLiveData: StateLiveData):
        for hive in stateLiveData.hives:
            if hive.hiveType == HiveType.HIVE_HEALTHY:
                hive.addZone(self.hiveZone(hive, stateLiveData))

    def hiveZone(self, hive: Hive, stateLiveData: StateLiveData):
        if self.checkIfObjectInArea(hive.pos, stateLiveData.fields[FieldsNames.TEAM1_ZONE.value]):
            return FieldsNames.TEAM1_ZONE
        elif self.checkIfObjectInArea(hive.pos, stateLiveData.fields[FieldsNames.TEAM2_ZONE.value]):
            return FieldsNames.TEAM2_ZONE
        return FieldsNames.NEUTRAL_ZONE

    def checkTimeLeft(self):
        if self.gameOn:
            return self.gameTime - (timer() - self.startTime)
        return self.gameTime

    @staticmethod
    def checkIfObjectInArea(objectPos: Point, field: Field):
        """Checks if object in area of map.
        Args:
            field: polygon defining the area
            objectPos (list): object x and y coordinates
        Returns:
            bool: True if object in area
        """
        point = SPoint(objectPos.reprTuple())
        polygon = SPolygon(field.reprTuple())
        return polygon.contains(point)

    def computeScore(self, stateLiveData: StateLiveData):
        team1DiseasedHivesCount = 0
        team2DiseasedHivesCount = 0

        for hive in stateLiveData.hives:
            # if there is a hive in team1 basket
            if self.checkIfObjectInArea(hive.pos, stateLiveData.fields[FieldsNames.TEAM1_BASKET.value]):
                # if it's healthy, increase score accordingly
                if hive.hiveType == HiveType.HIVE_HEALTHY:
                    self.score[0] += hive.getPoints(Config.TEAM1, stateLiveData.config)
                # if it's not healthy, increase count
                else:
                    team1DiseasedHivesCount += 1

            # if there is a hive in team2 basket
            elif self.checkIfObjectInArea(hive.pos, stateLiveData.fields[FieldsNames.TEAM2_BASKET.value]):
                # if it's healthy, increase score accordingly
                if hive.hiveType == HiveType.HIVE_HEALTHY:
                    self.score[1] += hive.getPoints(Config.TEAM2, stateLiveData.config)
                # if it's not healthy, increase count
                else:
                    team2DiseasedHivesCount += 1

        # compute scores for both teams
        self.teams[Config.TEAM1].score = \
            self.score[0] + team1DiseasedHivesCount * self.config.points['diseased'] + self.alterScore[0]
        self.teams[Config.TEAM2].score = \
            self.score[1] + team2DiseasedHivesCount * self.config.points['diseased'] + self.alterScore[1]

    def reprJSON(self, stateLiveData: StateLiveData):
        return {
            "objects": {
                "hives": {str(hive.id): hive.reprJSON(stateLiveData.config) for hive in stateLiveData.hives},
                "robots": {str(robot.id): robot.reprJSON() for robot in stateLiveData.robots}
            },
            "fields": {
                "baskets": {
                    "team1": stateLiveData.fields[FieldsNames.TEAM1_BASKET.value].reprJSON(),
                    "team2": stateLiveData.fields[FieldsNames.TEAM2_BASKET.value].reprJSON()
                },
                "zones": {
                    "team1": stateLiveData.fields[FieldsNames.TEAM1_ZONE.value].reprJSON(),
                    "team2": stateLiveData.fields[FieldsNames.TEAM2_ZONE.value].reprJSON(),
                    "neutral": stateLiveData.fields[FieldsNames.NEUTRAL_ZONE.value].reprJSON()
                },
                "field": stateLiveData.fields[FieldsNames.FIELD.value].reprJSON()
            },
            "teams": {
                "team1": self.teams[Config.TEAM1].reprJSON(),
                "team2": self.teams[Config.TEAM2].reprJSON()
            },
            "timeLeft": self.checkTimeLeft(),
            "gameOn": self.gameOn
        }
