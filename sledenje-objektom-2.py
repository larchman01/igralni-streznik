# -*- coding: utf-8 -*-

import logging
from multiprocessing import freeze_support

from gevent.pywsgi import WSGIServer

from so2.restapi.App import RESTAPI
from so2.servers.StateServer import StateServer
from so2.servers.TrackerServer import TrackerServer


def createLogger() -> logging.Logger:
    # create a logger
    loggerA = logging.getLogger('sledenje-objektom')
    loggerA.setLevel(logging.ERROR)

    # create a file handler
    file_handler = logging.FileHandler('example.log')
    file_handler.setLevel(logging.ERROR)

    # create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add handlers to the logger
    loggerA.addHandler(file_handler)
    loggerA.addHandler(console_handler)

    return loggerA


if __name__ == '__main__':
    logger = createLogger()
    logger.info('Started')
    freeze_support()
    game_servers = {}

    tracker_server = TrackerServer()
    tracker_server.start()

    state_server = StateServer(tracker_server)
    state_server.start()

    rest_app = RESTAPI(game_servers, state_server)
    rest_server = WSGIServer(('0.0.0.0', 8089), rest_app)
    rest_server.serve_forever()
