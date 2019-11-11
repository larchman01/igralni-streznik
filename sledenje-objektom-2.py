# -*- coding: utf-8 -*-

from gevent.pywsgi import WSGIServer

from so2.restapi.App import RESTAPI
from so2.servers.StateServer import StateServer
from so2.servers.TrackerServer import TrackerServer

game_servers = {}

tracker_server = TrackerServer()
state_server = StateServer(tracker_server)
state_server.start()

rest_app = RESTAPI(game_servers, state_server)
rest_server = WSGIServer(('', 8088), rest_app)
rest_server.serve_forever()

