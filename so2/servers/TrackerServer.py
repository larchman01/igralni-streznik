# -*- coding: utf-8 -*-

import gevent

from so2.servers.Server import Server


class TrackerServer(Server):
    """Tracker process babysitter

    Server spawns an external OpenCV tracker process and reads data from it.

    """

    def __init__(self):
        Server.__init__(self)

    def _run(self):
        # Start tracker in another process and open message queue
        while True:
            # Update state from tracker
            self.updated.set()
            gevent.sleep(0.01)
            self.updated.clear()
