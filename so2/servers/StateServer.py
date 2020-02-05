# -*- coding: utf-8 -*-import logging
import logging

import gevent
from sledilnik.classes.GameLiveData import GameLiveData

from so2.servers.Server import Server
from so2.servers.TrackerServer import TrackerServer


class StateServer(Server):
    """Server that stores abstract board information

    Server pulls information from the tracker server and serves the abstract description of the game board.

    Attributes:
        tracker: Tracker server
    """

    def __init__(self, tracker_server: TrackerServer):
        Server.__init__(self)
        self.logger = logging.getLogger('sledenje-objektom.StateServer')
        self.tracker: TrackerServer = tracker_server

    def _run(self):
        self.logger.info('State server started.')
        while True:
            self.tracker.updated.wait()

            self.state: GameLiveData = self.tracker.state
            self.updated.set()

            gevent.sleep(0.01)
            self.updated.clear()
