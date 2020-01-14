# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue

import gevent
from Tracker import Tracker

from so2.servers.Server import Server


class TrackerServer(Server):
    """Tracker process babysitter

    Server spawns an external OpenCV tracker process and reads data from it.

    """

    def __init__(self):
        Server.__init__(self)

        self.state = None
        self.queue = Queue()
        
        Tracker.ResFileNames.fieldsFilePath = 'fields.json'
        Tracker.ResFileNames.videoSource = './ROBO_3.mp4'

        self.p = Process(target=Tracker.start, args=(self.queue,))

    def _run(self):
        # Start tracker in another process and open message queue

        while True:
            # Update state from tracker

            if not self.p.is_alive():
                self.p.start()

            self.value = self.queue.get()
            self.updated.set(self.queue.get())
            gevent.sleep(0.01)
            self.updated.clear()
