from typing import List, Dict


class ConfigMap:
    def __init__(self):
        self.healthyHives: List = []
        self.diseasedHives: List = []
        self.teams: Dict[int, str]
