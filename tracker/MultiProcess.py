import multiprocessing
import time
import concurrent.futures


def do_something(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    return f"Done sleeping...{seconds}"


if __name__ == '__main__':
    start = time.perf_counter()
    #
    # p1 = multiprocessing.Process(target=do_something)
    # p2 = multiprocessing.Process(target=do_something)
    #
    # p1.start()
    # p2.start()
    #
    # p1.join()
    # p2.join()
    #

    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]

        results = executor.map(do_something, secs)

        # for result in results:
        #     print(result)

        # results = [executor.submit(do_something, sec) for sec in secs]
        #
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     f1 = executor.submit(do_something, 1)
    #     f2 = executor.submit(do_something, 1)
    #     print(f1.result())
    #     print(f2.result())

    finish = time.perf_counter()

    print(f"Time: {round(finish - start, 3)} second(s)")
