# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue

import gevent
from sledilnik.Tracker import Tracker

from so2.servers.Server import Server


class TrackerServer(Server):
    """Tracker process babysitter

    Server spawns an external OpenCV tracker process and reads data from it.

    """

    def __init__(self):
        Server.__init__(self)

        self.state = None
        self.queue = Queue()

        self.tracker = Tracker()
        # self.tracker.setDebug()
        self.tracker.setVideoSource('./so2/tracker/ROBO_3.mp4')

        self.p = Process(target=self.tracker.start, args=(self.queue,))

    def getValue(self):
        if not self.queue.empty():
            return self.queue.get()

    def _run(self):
        # Start tracker in another process and open message queue
        self.p.start()

        while True:
            # Update state from tracker

            if not self.p.is_alive():
                self.p = Process(target=self.tracker.start, args=(self.queue,))
                self.p.start()

            self.updated.set()
            gevent.sleep(0.03)
            self.updated.clear()
