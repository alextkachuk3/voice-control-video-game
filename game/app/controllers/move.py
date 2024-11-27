import pygame as pg

from app.controllers.controller import Controller


class MoveController(Controller):
    def __init__(self, rect, default_state:str, default_side:int, speed:int):
        super().__init__(rect, default_state)
        self._side = default_side
        self._speed = speed

    def _move_object(self, direction: pg.math.Vector2):
        self._rect.center += self._speed * direction

    def move(self):
        pass

    def set_side(self, side):
        self._side = side

