class Storage:
    __storage = {}

    def set(self, key, value):
        self.__storage[key] = value

    def get(self, key, default=None):
        return self.__storage.get(key, default)

    def contains(self, key):
        return key in self.__storage