import pygame as pg

from app import consts
from app.controllers.attack import MagicController
from app.controllers.move import MoveController


class NetworkMoveController(MoveController):
    def __init__(self, owner, default_state=consts.IDLE, default_side=pg.K_a, speed=0, database_ref=None, pos=(0, 0)):
        super().__init__(owner, default_state, default_side, speed)

        self.__stream = None
        if database_ref:
            self.__stream = database_ref.stream(self.__update)

        self.__x, self.__y = pos

    def __update(self, message):
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        data = message["data"]

        if data is None:
            return

        self.__x = data["x"]
        self.__y = data["y"]
        self._state = data["state"]
        self._side = data["side"]

        self._call_all(state=self._state, side=self._side)


    def move(self):
        if self._state not in [consts.IDLE, consts.RUN] or not self._owner.alive():
            return

        self._owner.rect.center = (self.__x, self.__y)

    def close(self):
        if self.__stream:
            self.__stream.close()


class NetworkMagicController(MagicController):
    def __init__(self, owner, default_state=consts.IDLE, database_ref=None):
        super().__init__(owner, default_state)

        self._mouse_pos = (0, 0)

        self.__stream = None
        if database_ref:
            self.__stream = database_ref.stream(self.__update)

    def __update(self, message):
        if self._state not in [consts.IDLE, consts.RUN]:
            return
        data = message["data"]
        if data is None:
            return

        self._state = data["state"]
        self._mouse_pos = data["mousex"], data["mousey"]
        self._attack_event(self._state, self._mouse_pos)
        self._call_all(state=self._state)


    def close(self):
        if self.__stream:
            self.__stream.close()
