from multiprocessing import Process, Queue
import time

from tracker import Tracker

if __name__ == '__main__':

    queue = Queue()

    # Creates Tracker process with multiprocess queue as argument
    p = Process(target=Tracker.startTracker, args=(queue, ))

    # Starts Tracker process
    p.start()

    # Prints array
    times = []
    start = time.perf_counter()
    for _ in range(100):
        gameData = queue.get()

    end = time.perf_counter()
    print(f"average time: {round((end - start) / 100, 3)}")
