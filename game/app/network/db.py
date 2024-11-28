from threading import Thread
import pyrebase

from app.network.configs import confs

class AsyncDatabase:
    def __init__(self, database):
        self.__database = database


    def child(self, path:str | list[str]):
        if isinstance(path, str):
            path = path.split("/")
        node = self.__database
        for key in path:
            node = node.child(key)

        return AsyncDatabase(node)
    def __async_push(self, data, callback):
        res = self.__database.push(data)
        callback(res)

    def push(self, data, callback=lambda res: res):
        thread = Thread(target=self.__async_push, args=(data, callback))
        thread.start()

    def __async_set(self, data, callback):
        res = self.__database.set(data)
        callback(res)

    def set(self, data, callback=lambda res: res):
        thread = Thread(target=self.__async_set, args=(data, callback))
        thread.start()

    def __async_get(self, callback):
        res = self.__database.get()
        callback(res)

    def get(self, callback=lambda res: res):
        thread = Thread(target=self.__async_get, args=(callback, ))
        thread.start()

    def stream(self, callback):
        return self.__database.stream(callback)


firebase = pyrebase.initialize_app(confs)
database = firebase.database()
