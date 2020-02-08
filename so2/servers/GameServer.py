# -*- coding: utf-8 -*-
import logging
from typing import Dict
from uuid import uuid4

import gevent
from sledilnik.classes.Field import Field
from sledilnik.classes.Point import Point

from so2.entities.GameLiveData import GameLiveData
from so2.entities.Hive import Hive
from so2.enums.FieldsNamesEnum import FieldsNames
from so2.enums.HiveTypeEnum import HiveType
from so2.servers.Server import Server
from so2.servers.StateServer import StateServer

from shapely.geometry import Point as SPoint
from shapely.geometry.polygon import Polygon as SPolygon


class GameServer(Server):
    """Game state for particular game

    Pulls information from a state server and computers a game state.

    Attributes:
        id (UUID): Game id
        key (string): Key for write permissions
    """

    def __init__(self, state_server: StateServer):
        Server.__init__(self)

        # init server
        self.logger = logging.getLogger('sledenje-objektom.GameServer')
        self.state_server = state_server
        self.id = str(uuid4())[:4]
        self.key = "very_secret_key"

        # init game
        self.first = True
        self.hivesStartingZones: Dict[int, FieldsNames] = {}

        self.team1Score = 0
        self.team2Score = 0

    def _run(self):
        self.logger.info("Started a new game server with id: %s" % self.id)
        while True:
            # Wait for state server to update state
            self.state_server.updated.wait()
            self.gameData: GameLiveData = self.state_server.state

            if self.gameData.gameOn:
                if self.first:
                    self.initGame()

                self.computeScore()

            else:
                self.first = True

            self.updated.set()
            gevent.sleep(0.01)
            self.updated.clear()

    def initGame(self):

        self.first = False

        self.team1Score = 0
        self.team2Score = 0

        # if the game has just started, remember hive's starting zone
        for hiveId, hive in self.gameData.hives.items():
            if hive.hiveType == HiveType.HIVE_HEALTHY:
                self.hivesStartingZones[hiveId] = self.hiveZone(hive)

    def hiveZone(self, hive: Hive):
        if self.checkIfObjectInArea(hive.pos, self.gameData.fields[FieldsNames.TEAM1_ZONE.value]):
            return FieldsNames.TEAM1_ZONE
        elif self.checkIfObjectInArea(hive.pos, self.gameData.fields[FieldsNames.TEAM2_ZONE.value]):
            return FieldsNames.TEAM2_ZONE
        return FieldsNames.NEUTRAL_ZONE

    def computeScore(self):
        team1DiseasedHivesCount = 0
        team2DiseasedHivesCount = 0

        for hiveId, hive in self.gameData.hives:
            # if there is a hive in team1 basket
            if self.checkIfObjectInArea(hive.pos, self.gameData.fields[FieldsNames.TEAM1_BASKET.value]):
                # if it's healthy, increase score accordingly
                if hive.hiveType == HiveType.HIVE_HEALTHY:
                    if self.hivesStartingZones[hiveId] == FieldsNames.TEAM2_ZONE:
                        self.team1Score += self.gameData.config.points['enemy']
                    elif self.hivesStartingZones[hiveId] == FieldsNames.NEUTRAL_ZONE:
                        self.team1Score += self.gameData.config.points['neutral']
                    else:
                        self.team1Score += self.gameData.config.points['home']
                # if it's not healthy, increase count
                else:
                    team1DiseasedHivesCount += 1

            # if there is a hive in team2 basket
            elif self.checkIfObjectInArea(hive.pos, self.gameData.fields[FieldsNames.TEAM2_BASKET.value]):
                # if it's healthy, increase score accordingly
                if hive.hiveType == HiveType.HIVE_HEALTHY:
                    if self.hivesStartingZones[hiveId] == FieldsNames.TEAM1_ZONE:
                        self.team2Score += self.gameData.config.points['enemy']
                    elif self.hivesStartingZones[hiveId] == FieldsNames.NEUTRAL_ZONE:
                        self.team2Score += self.gameData.config.points['neutral']
                    else:
                        self.team2Score += self.gameData.config.points['home']
                # if it's not healthy, increase count
                else:
                    team2DiseasedHivesCount += 1

        # compute scores for both teams
        self.gameData.teams[0].score = \
            self.team1Score - team1DiseasedHivesCount * self.gameData.config.points['diseased']
        self.gameData.teams[1].score = \
            self.team2Score - team2DiseasedHivesCount * self.gameData.config.points['diseased']

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
