from multiprocessing import Queue

from Tracker import Tracker

Tracker.ResFileNames.videoSource = 'ROBO_3.mp4'
Tracker.debug = True
queue = Queue()

try:
    Tracker.start(queue)
except:
    while not queue.empty():
        print(queue.get())
