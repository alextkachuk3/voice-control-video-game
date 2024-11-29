class Storage:
    __storage = {}

    @staticmethod
    def set(key, value):
        Storage.__storage[key] = value

    @staticmethod
    def get(key, default=None):
        return Storage.__storage.get(key, default)

    @staticmethod
    def contains(key):
        return key in Storage.__storage
