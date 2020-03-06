# -*- coding: utf-8 -*-
import logging
from timeit import default_timer as timer
from typing import Dict, List
from uuid import uuid4

import gevent

from so2.entities.GameLiveData import GameLiveData
from so2.entities.StateLiveData import StateLiveData
from so2.enums.ConfigEnum import Config
from so2.servers.Server import Server
from so2.servers.StateServer import StateServer


class GameServer(Server):
    """Game state for particular game

    Pulls information from a state server and computers a game state.

    Attributes:
        id (UUID): Game id
        key (string): Key for write permissions
    """

    def __init__(self, state_server: StateServer, team1RobotId: int, team2RobotId: int):
        Server.__init__(self)

        # init server
        self.logger = logging.getLogger('sledenje-objektom.GameServer')
        self.state_server = state_server
        self.id = str(uuid4())[:4]
        self.key = "very_secret_key"
        self.gameData: GameLiveData = GameLiveData(team1RobotId, team2RobotId)
        self.stateData: StateLiveData

    def _run(self):
        self.logger.info("Started a new game server with id: %s" % self.id)
        while True:
            # Wait for state server to update state
            self.state_server.updated.wait()
            self.stateData: StateLiveData = self.state_server.state

            # print(self.id, self.gameData.gameOn)
            if self.gameData.gameOn:
                self.gameData.checkHiveZones(self.stateData)
                self.gameData.computeScore(self.stateData)
                # stop the game when no time left
                if self.gameData.checkTimeLeft() <= 0:
                    self.gameData.gameOn = False
                    self.gameData.startTime = timer()
                    break
            else:
                self.gameData.startTime = timer()

            self.updated.set()
            gevent.sleep(0.01)
            self.updated.clear()

    def alterScore(self, scores: Dict[str, int]):

        self.gameData.alterScore[0] = scores['team1']
        self.gameData.alterScore[1] = scores['team2']

        return {
            'team1': self.gameData.teams[Config.TEAM1].score,
            'team2': self.gameData.teams[Config.TEAM2].score
        }

    def startGame(self):
        self.gameData.startGame()

    def stopGame(self):
        self.gameData.gameOn = False

    def setTeams(self, robotIds: List[str]):
        self.gameData.teams = {}
        self.gameData.addTeam(Config.TEAM1, robotIds[0])
        self.gameData.addTeam(Config.TEAM2, robotIds[1])

    def setGameTime(self, gameTime: int):
        self.gameData.gameTime = gameTime

    def reprJSON(self):
        return self.gameData.reprJSON(self.stateData)
