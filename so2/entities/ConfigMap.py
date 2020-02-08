import json
import logging
import os
from typing import List, Dict


class ConfigMap:
    def __init__(self):
        self.logger = logging.getLogger('sledenje-objektom.ConfigMap')
        self.healthyHives: List = []
        self.diseasedHives: List = []
        self.teams: Dict[str, str] = {}
        self.points: Dict[str, int] = {}
        self.gameTime: int = 100
        self.readConfig()

    def readConfig(self):
        if os.path.isfile('config.json'):
            with open('config.json') as jsonFile:
                jsonConfig = json.load(jsonFile)
                self.parseJSON(jsonConfig)
        else:
            self.logger.critical("Can't load config.json!")
            quit(-1)

    def parseJSON(self, jsonData):
        self.healthyHives = jsonData['healthyHives']
        self.diseasedHives = jsonData['diseasedHives']
        self.teams = jsonData['teams']
        self.points = jsonData['points']
        self.gameTime = jsonData['gameTime']
