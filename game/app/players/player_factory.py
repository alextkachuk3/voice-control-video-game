class PlayerFactory(type):
    __players = {}

    def __new__(cls, name, bases, attrs):
        class_ = super().__new__(cls, name, bases, attrs)

        if "__title__" in attrs and ("__abstract__" not in attrs or not attrs["__abstract__"]):
            PlayerFactory.__players[attrs["__title__"]] = class_

        return class_

    @staticmethod
    def spawn(title, *args, **kwargs):
        if title in PlayerFactory.__players:
            return PlayerFactory.__players[title](*args, **kwargs)
        raise TypeError("Player '{}' is not registered.".format(title))

    @staticmethod
    def keys():
        return list(PlayerFactory.__players.keys())
