import pygame as pg
from typing import Any

from app.base.animator import Animator, Animation


class AnimateController(Animator):
    def __init__(self, side_mapper: dict[int, int], animations: dict[Any, Animation], default=None):
        super().__init__(animations, default)
        self.__side = pg.K_a

        self.__side_mapper = side_mapper

        self.replace_row(self.__side_mapper[self.__side])

    def move(self, side):
        self.__side = side
        self.replace_row(self.__side_mapper[self.__side])

    @property
    def side(self):
        return self.__side