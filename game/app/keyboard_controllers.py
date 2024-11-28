import pygame as pg

from app import consts
from app.controllers.attack import MagicController
from app.controllers.move import MoveController
from app.utility import SIDE_DIRECTION


class KeyboardMoveController(MoveController):
    def __init__(self, rect, default_state=consts.IDLE, default_side=pg.K_a, speed=0):
        super().__init__(rect, default_state, default_side, speed)

    def move(self):
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        pressed = pg.key.get_pressed()
        direction = pg.math.Vector2(0, 0)
        self._state = consts.IDLE

        if pressed[pg.K_a]:
            self._side = pg.K_a
        elif pressed[pg.K_d]:
            self._side = pg.K_d

        if pressed[pg.K_w]:
            self._side = pg.K_w
        elif pressed[pg.K_s]:
            self._side = pg.K_s

        if pressed[pg.K_a] or pressed[pg.K_d] or pressed[pg.K_w] or pressed[pg.K_s]:
            self._state = consts.RUN
            direction += SIDE_DIRECTION[self._side]

        self._call_all(state=self._state, side=self._side)
        self._move_object(direction)

class KeyboardMagicController(MagicController):
    def attack(self):
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        pressed = pg.key.get_pressed()

        if pressed[pg.K_1]:
            self._state = consts.ATTACK1
        elif pressed[pg.K_2]:
            self._state = consts.ATTACK2
        elif pressed[pg.K_3]:
            self._state = consts.ATTACK3

        self._attack_event(self._state, pg.mouse.get_pos())