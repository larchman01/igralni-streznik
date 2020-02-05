class Team:
    def __init__(self, teamId, name):
        self.id = teamId
        self.name = name
        self.score = 0

    def reprJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score
        }
