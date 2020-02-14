# -*- coding: utf-8 -*-
from typing import Dict

import orjson
from flask import Flask, request

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
            return game_servers[game_id].reprJSON()
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

    @app.route("/game/<string:game_id>/score", methods=["POST"])
    def alter_score(game_id):
        if game_id in game_servers:
            game_server = game_servers[game_id]
            return game_server.alterScore(request.json)
        else:
            return error("Igra s takšnim id-jem ne obstaja!")

    @app.route("/game/<string:game_id>/start", methods=["PUT"])
    def start_game(game_id):
        if game_id in game_servers:
            game_server = game_servers[game_id]
            game_server.gameData.gameOn = True
            return True
        else:
            return error("Igra s takšnim id-jem ne obstaja!")

    @app.route("/game/<string:game_id>/stop", methods=["PUT"])
    def stop_game(game_id):
        if game_id in game_servers:
            game_server = game_servers[game_id]
            game_server.gameData.gameOn = False
            return True
        else:
            return error("Igra s takšnim id-jem ne obstaja!")

    @app.route("/game/<string:game_id>/time", methods=["POST"])
    def set_game(game_id):
        if game_id in game_servers:
            game_server = game_servers[game_id]
            game_server.gameData.config.gameTime = request.json['gameTime']
            return True
        else:
            return error("Igra s takšnim id-jem ne obstaja!")

    @app.route("/game/<string:game_id>/teams", methods=["POST"])
    def set_game(game_id):
        if game_id in game_servers:
            game_server = game_servers[game_id]
            game_server.setTeams(request.json['teams'])
            return True
        else:
            return error("Igra s takšnim id-jem ne obstaja!")

    @app.route("/teams", methods=['GET'])
    def get_teams():
        return state_server.gameLiveData.config.teams

    @app.errorhandler(400)
    def error(msg: str):
        return msg, 400

    return app
