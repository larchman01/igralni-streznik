from typing import Dict


class Team:
    def __init__(self, teamId, name):
        self.id = teamId
        self.name = name
        self.score = 0
        self.scoreAdjust = 0
        self.healthyHives: Dict[int, int] = {}

    def reprJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score
        }
