# -*- coding: utf-8 -*-

import orjson

from flask import Flask

from so2.servers.GameServer import GameServer


def RESTAPI(game_servers, state_server):
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def index():
        return "{}"

    @app.route("/game/<uuid:game_id>", methods=["GET"])
    def game(game_id):
        return game_servers[game_id].getJSON()

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

    return app
