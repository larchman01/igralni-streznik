# -*- coding: utf-8 -*-
from typing import Dict

import orjson
from flask import Flask

from so2.servers.GameServer import GameServer
from so2.servers.StateServer import StateServer


def RESTAPI(game_servers: Dict[str, GameServer], state_server: StateServer):
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def index():
        return "{}"

    @app.route("/game/<string:game_id>", methods=["GET"])
    def game(game_id):
        if game_id in game_servers:
            gameData = game_servers[game_id].gameData
            return gameData.reprJSON()
        else:
            return error("Igra s takšnim id-jem ne obstaja!")

    @app.route("/game", methods=["PUT"])
    def create_game():
        new_game = GameServer(state_server)
        game_servers[new_game.id] = new_game
        new_game.start()
        return str(new_game.id)

    @app.route("/game", methods=["GET"])
    def get_games():
        games = [str(game_id) for game_id in game_servers]
        return orjson.dumps(games)

    @app.errorhandler(400)
    def error(msg: str):
        return msg, 400

    return app
