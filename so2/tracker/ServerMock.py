import time
from multiprocessing import Process, Queue

from Tracker import Tracker

if __name__ == '__main__':

    queue = Queue()
    Tracker.ResFileNames.videoSource = 'ROBO_3.mp4'
    # Creates Tracker process with multiprocess queue as argument
    p = Process(target=Tracker.start, args=(queue,))

    # Starts Tracker process
    p.start()

    print(queue.get())

    # Prints array
    times = []
    start = time.perf_counter()
    for _ in range(100):
        gameData = queue.get()
        print("Hm: " + gameData)

    end = time.perf_counter()
    print(f"average time: {round((end - start) / 100, 3)}")
