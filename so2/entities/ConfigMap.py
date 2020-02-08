from typing import List, Dict


class ConfigMap:
    def __init__(self):
        self.healthyHives: List = []
        self.diseasedHives: List = []
        self.teams: Dict[str, str] = {}
        self.team1RobotId: str = '-1'
        self.team2RobotId: str = '-2'
        self.points: Dict[str, int] = {}

    def parseJSON(self, json):
        self.healthyHives = json['healthyHives']
        self.diseasedHives = json['diseasedHives']
        self.teams = json['teams']
        self.team1RobotId = str(json['players']['team1'])
        self.team2RobotId = str(json['players']['team2'])
        self.points = json['points']
