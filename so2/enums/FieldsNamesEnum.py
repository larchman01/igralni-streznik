from enum import Enum


# this has to match with fields.json
class FieldsNames(Enum):
    FIELD = "poligon"
    TEAM1_BASKET = "kosara ekipe 1"
    TEAM2_BASKET = "kosara ekipe 2"
    TEAM1_ZONE = "cona ekipe 1"
    TEAM2_ZONE = "cona ekipe 2"
    NEUTRAL_ZONE = "nevtralna cona"
