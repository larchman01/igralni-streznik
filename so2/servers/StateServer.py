# -*- coding: utf-8 -*-

import gevent

from so2.servers import TrackerServer
from so2.servers.Server import Server


# class ResGameLiveData:
#     def __init__(self, configMap):
#         self.fields = configMap.fields
#         self.objects = {}
#
#     def write(self, objects):
#         self.objects.clear()
#         for id, obj in objects.items():
#             self.objects[id] = MovableObject(id, obj.position[0], obj.position[1], obj.direction)


class StateServer(Server):
    """Server that stores abstract board information

    Server pulls information from the tracker server and serves the abstract description of the game board.

    Attributes:
        tracker: Tracker server
    """

    def __init__(self, tracker_server: TrackerServer):
        Server.__init__(self)
        self.tracker: TrackerServer = tracker_server

    def getGameData(self):
        return self.tracker.getValue()

    def _run(self):
        while True:
            self.tracker.updated.wait()
            # Update state from tracker

            # game_data = self.tracker.getValue()
            # print(game_data.fields)
            # print(game_data.objects)

            self.updated.set()
            gevent.sleep(0.03)
            self.updated.clear()
