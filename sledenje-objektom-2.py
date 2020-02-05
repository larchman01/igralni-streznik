# -*- coding: utf-8 -*-

import logging
from multiprocessing import freeze_support

from gevent.pywsgi import WSGIServer

from so2.restapi.App import RESTAPI
from so2.servers.GameServer import GameServer
from so2.servers.StateServer import StateServer
from so2.servers.TrackerServer import TrackerServer


def createLogger() -> logging.Logger:
    # create a logger
    logger = logging.getLogger('sledenje-objektom')
    logger.setLevel(logging.DEBUG)

    # create a file handler
    file_handler = logging.FileHandler('example.log')
    file_handler.setLevel(logging.DEBUG)

    # create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    logger = createLogger()
    logger.info('Started')
    freeze_support()
    game_servers = {}

    tracker_server = TrackerServer()
    tracker_server.start()

    state_server = StateServer(tracker_server)
    state_server.start()

    new_game = GameServer(state_server)
    print(new_game.id);
    game_servers[new_game.id] = new_game
    new_game.start()

    rest_app = RESTAPI(game_servers, state_server)
    rest_server = WSGIServer(('', 8088), rest_app)
    rest_server.serve_forever()
