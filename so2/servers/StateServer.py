# -*- coding: utf-8 -*-

import gevent

from so2.servers import TrackerServer
from so2.servers.Server import Server


class StateServer(Server):
    """Server that stores abstract board information

    Server pulls information from the tracker server and serves the abstract description of the game board.

    Attributes:
        tracker: Tracker server
    """

    def __init__(self, tracker_server: TrackerServer):
        Server.__init__(self)
        self.tracker = tracker_server

    def _run(self):
        while True:
            self.tracker.updated.wait()
            # Update state from tracker
            self.state = self.tracker.value
            self.value = self.state

            self.updated.set()
            gevent.sleep(0.01)
            self.updated.clear()
