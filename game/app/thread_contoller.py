import multiprocessing as mp

class ThreadController:
    __queue = mp.Queue()

    @staticmethod
    def run_on_main(func, *args, **kwargs):
        ThreadController.__queue.put((func, args, kwargs))

    @staticmethod
    def get():
        return ThreadController.__queue.get()

    @staticmethod
    def empty():
        return ThreadController.__queue.empty()


