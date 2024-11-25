import pygame as pg

from app import consts
from app.controllers.attack import MagicController
from app.controllers.move import MoveController
from app.utility import SIDE_DIRECTION


class NetworkMoveController(MoveController):
    def __init__(self, rect, default_state=consts.IDLE, default_side=pg.K_a, speed=0, database_ref=None):
        super().__init__(rect, default_state, default_side, speed)

        if database_ref:
            database_ref.stream(self.__update_pos)

        self.__x = 0
        self.__y = 0

    def __update_pos(self, message):
        print(message)
        if "move" in message["path"]:
            data = message["data"]
            self.__x = data["x"]
            self.__y = data["y"]
            self._state = data["state"]
            self._side = data["side"]

    def move(self):
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        direction = pg.math.Vector2(0, 0)

        if self._state == consts.RUN:
            direction += SIDE_DIRECTION[self._side]

        self._call_all(state=self._state, side=self._side)
        self._move_object(direction)

class NetworkMagicController(MagicController):
    def __init__(self, rect, default_state=consts.IDLE, owner=None, database_ref=None):
        super().__init__(rect, default_state, owner)

        if database_ref:
            database_ref.stream(self.__update_attack)

    def __update_attack(self, message):
        print(message)
        if "attack" in message["path"]:
            data = message["data"]
            self._state = data["state"]

    def attack(self):
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        self._attack_event(self._state)