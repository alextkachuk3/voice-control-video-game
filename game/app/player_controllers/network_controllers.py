import pygame as pg

from app import consts
from app.controllers.attack import MagicController
from app.controllers.move import MoveController


class NetworkMoveController(MoveController):
    def __init__(self, rect, default_state=consts.IDLE, default_side=pg.K_a, speed=0, database_ref=None):
        super().__init__(rect, default_state, default_side, speed)

        self.__stream = None
        if database_ref:
            self.__stream = database_ref.stream(self.__update)

        self.__x = 0
        self.__y = 0

    def __update(self, message):
        print(message)
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        if message["path"].endswith("move"):
            data = message["data"]
            self.__x = data["x"]
            self.__y = data["y"]
            self._state = data["state"]
            self._side = data["side"]

            self._call_all(state=self._state, side=self._side)

    def move(self):
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        self._rect.center = (self.__x, self.__y)

    def close(self):
        if self.__stream:
            self.__stream.close()

class NetworkMagicController(MagicController):
    def __init__(self, rect, default_state=consts.IDLE, owner=None, database_ref=None):
        super().__init__(rect, default_state, owner)

        self._mouse_pos = (0, 0)

        self.__stream = None
        if database_ref:
            self.__stream = database_ref.stream(self.__update)

    def __update(self, message):
        print(message)
        if self._state not in [consts.IDLE, consts.RUN]:
            return
        if message["path"].endswith("attack"):
            data = message["data"]
            self._state = data["state"]
            self._mouse_pos = data["mousex"], data["mousey"]
            self._attack_event(self._state, self._mouse_pos)
            self._call_all(state=self._state)

    def close(self):
        if self.__stream:
            self.__stream.close()