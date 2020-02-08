# -*- coding: utf-8 -*-
import logging
from typing import Dict, List
from uuid import uuid4

import gevent

from so2.entities.GameLiveData import GameLiveData
from so2.entities.StateLiveData import StateLiveData
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

            if self.gameData.gameOn:
                self.gameData.computeScore(self.stateData)

            else:
                self.first = True

            self.updated.set()
            gevent.sleep(0.01)
            self.updated.clear()

    def alterScore(self, scores: Dict[str, int]):

        self.gameData.score[0] += scores['team1']
        self.gameData.score[1] += scores['team2']

        return {
            'team1': self.gameData.score[0],
            'team2': self.gameData.score[1]
        }

    def startGame(self):
        self.gameData.startGame(self.stateData)

    def stopGame(self):
        self.gameData.gameOn = False

    def setTeams(self, robotIds: List[str]):
        self.gameData.teams = []
        self.gameData.addTeam(robotIds[0])
        self.gameData.addTeam(robotIds[1])

    def setGameTime(self, gameTime: int):
        self.gameData.gameTime = gameTime

    def reprJSON(self):
        return self.gameData.reprJSON(self.stateData)
