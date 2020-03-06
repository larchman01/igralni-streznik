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
          "x": 2,
          "y": 503
        },
        "bottomRight": {
          "x": 507,
          "y": 503
        },
        "topLeft": {
          "x": 1,
          "y": 1541
        },
        "topRight": {
          "x": 529,
          "y": 1551
        }
      },
      "team2": {
        "bottomLeft": {
          "x": 3049,
          "y": 505
        },
        "bottomRight": {
          "x": 3554,
          "y": 514
        },
        "topLeft": {
          "x": 3037,
          "y": 1550
        },
        "topRight": {
          "x": 3549,
          "y": 1545
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
          "x": 1035,
          "y": 1
        },
        "bottomRight": {
          "x": 2547,
          "y": -7
        },
        "topLeft": {
          "x": 1013,
          "y": 2042
        },
        "topRight": {
          "x": 2540,
          "y": 2044
        }
      },
      "team1": {
        "bottomLeft": {
          "x": -3,
          "y": 0
        },
        "bottomRight": {
          "x": 1021,
          "y": 1
        },
        "topLeft": {
          "x": 0,
          "y": 2052
        },
        "topRight": {
          "x": 1010,
          "y": 2048
        }
      },
      "team2": {
        "bottomLeft": {
          "x": 2547,
          "y": -1
        },
        "bottomRight": {
          "x": 3560,
          "y": 3
        },
        "topLeft": {
          "x": 2540,
          "y": 2049
        },
        "topRight": {
          "x": 3558,
          "y": 2052
        }
      }
    }
  },
  "gameOn": false,
  "objects": {
    "hives": {
      "42": {
        "dir": -4217.568666877783,
        "id": 42,
        "points": {
          "team1": 1,
          "team2": 1
        },
        "position": {
          "x": 558,
          "y": 318
        },
        "type": "HIVE_DISEASED"
      },
      "47": {
        "dir": -5402.370539603227,
        "id": 47,
        "points": {
          "team1": 1,
          "team2": 1
        },
        "position": {
          "x": 567,
          "y": 1710
        },
        "type": "HIVE_HEALTHY"
      }
    },
    "robots": {
      "25": {
        "dir": 172.23483398157467,
        "id": 25,
        "position": {
          "x": 3056,
          "y": 455
        }
      }
    }
  },
  "teams": {
    "team1": {
      "id": 0,
      "name": "Acvirki",
      "score": 0
    },
    "team2": {
      "id": 25,
      "name": "LASPP",
      "score": 0
    }
  },
  "timeLeft": 100
}
```

#### PUT `/game`
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
 "gameTime": 120
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
 "team1": 2,
 "team2": 3
}
```

#### GET `/teams`
##### Response:
```json
[
 {"id": "0", "name": "Super Glavce"},
 {"id": "5", "name": "GAYA"},
 {"id": "12", "name": "Distopija"}
]
```