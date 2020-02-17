## API ENDPOINTS

#### GET `/game`

##### Response:
```json
["game1", "game2", "game3"]
```

#### GET `/game/{game_id}`
##### Response:
```json
{
  "fields": {
    "baskets": {
      "team1": {
        "bottomLeft": {
          "x": -30,
          "y": 493
        },
        "bottomRight": {
          "x": 549,
          "y": 488
        },
        "topLeft": {
          "x": 15,
          "y": 1537
        },
        "topRight": {
          "x": 575,
          "y": 1547
        }
      },
      "team2": {
        "bottomLeft": {
          "x": 3016,
          "y": 544
        },
        "bottomRight": {
          "x": 3557,
          "y": 527
        },
        "topLeft": {
          "x": 3065,
          "y": 1587
        },
        "topRight": {
          "x": 3598,
          "y": 1570
        }
      }
    },
    "field": {
      "bottomLeft": {
        "x": 0,
        "y": 0
      },
      "bottomRight": {
        "x": 3555,
        "y": 0
      },
      "topLeft": {
        "x": 0,
        "y": 2055
      },
      "topRight": {
        "x": 3555,
        "y": 2055
      }
    },
    "zones": {
      "neutral": {
        "bottomLeft": {
          "x": 996,
          "y": 20
        },
        "bottomRight": {
          "x": 2540,
          "y": 0
        },
        "topLeft": {
          "x": 1017,
          "y": 2070
        },
        "topRight": {
          "x": 2533,
          "y": 2072
        }
      },
      "team1": {
        "bottomLeft": {
          "x": 13,
          "y": -17
        },
        "bottomRight": {
          "x": 1012,
          "y": 3
        },
        "topLeft": {
          "x": 10,
          "y": 2063
        },
        "topRight": {
          "x": 1009,
          "y": 2057
        }
      },
      "team2": {
        "bottomLeft": {
          "x": 2529,
          "y": -3
        },
        "bottomRight": {
          "x": 3550,
          "y": -9
        },
        "topLeft": {
          "x": 2538,
          "y": 2072
        },
        "topRight": {
          "x": 3539,
          "y": 2055
        }
      }
    }
  },
  "gameOn": false,
  "objects": {
    "hives": {},
    "robots": {
      "25": {
        "dir": 76.2930389959202,
        "id": 25,
        "position": {
          "x": 2146,
          "y": 1528
        }
      }
    }
  },
  "teams": {
    "team1": {
      "id": 0,
      "name": "Team1Name",
      "score": 0
    },
    "team2": {
      "id": 25,
      "name": "Team2Name",
      "score": 0
    }
  },
  "timeLeft": 100
}
```

#### PUT `/game`
##### Response:
```json
{
 "gameId": "3f4e"
}
```

#### POST `/game/{game_id}/score`
##### Request:
```json
{
 "team1": 2,
 "team2": 3
}
```
##### Response:
```json
{
 "team1": 2,
 "team2": 3
}
```

#### PUT `/game/{game_id}/start`
##### Response:
```json
{
 "gameOn": "True"
}
```

#### PUT `/game/{game_id}/stop`
##### Response:
```json
{
 "gameOn": "False"
}
```

#### POST `/game/{game_id}/time`
##### Response:
```json
{
 "gameTime": "120"
}
```

#### POST `/game/{game_id}/teams
##### Request example:
```json
{
 "team1": 2,
 "team2": 3
}
```
##### Response:
```json
{
 "team1": "2",
 "team2": "3"
}
```

#### GET `/teams`
##### Response:
```json
  {
    "0": "Team1",
    "1": "Team2",
    "2": "Team3"
  }
```