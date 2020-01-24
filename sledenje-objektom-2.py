# -*- coding: utf-8 -*-

from gevent.pywsgi import WSGIServer

from multiprocessing import freeze_support
from so2.restapi.App import RESTAPI
from so2.servers.GameServer import GameServer
from so2.servers.StateServer import StateServer
from so2.servers.TrackerServer import TrackerServer


if __name__ == '__main__':
    freeze_support()
    game_servers = {}

    tracker_server = TrackerServer()
    tracker_server.start()
    state_server = StateServer(tracker_server)
    state_server.start()

    new_game = GameServer(state_server)
    game_servers[new_game.id] = new_game
    print(new_game.id)
    new_game.start()

    rest_app = RESTAPI(game_servers, state_server)
    rest_server = WSGIServer(('', 8088), rest_app)
    rest_server.serve_forever()

