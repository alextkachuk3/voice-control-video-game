import pygame as pg

from app.controllers.controller import Controller


class MoveController(Controller):
    def __init__(self, owner, default_state:str, default_side:int, speed:int):
        super().__init__(owner, default_state)
        self._side = default_side
        self._speed = speed

    def _move_object(self, direction: pg.math.Vector2):
        if self._owner.alive():
            self._owner.rect.center += self._speed * direction

    def move(self):
        pass

    def set_side(self, side):
        self._side = side

    @property
    def side(self):
        return self._side

    @property
    def speed(self):
        return self._speed


