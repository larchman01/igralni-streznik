from sledilnik.classes.MovableObject import MovableObject

from so2.enums.HiveTypeEnum import HiveType


class Hive(MovableObject):
    def __init__(self, obj: MovableObject, hiveType: HiveType):
        super().__init__(obj.x, obj.y, obj.direction)
        self.hiveType: HiveType = hiveType

    def reprJSON(self):
        json = super().reprJSON()
        json["type"] = self.hiveType.value
        return json
