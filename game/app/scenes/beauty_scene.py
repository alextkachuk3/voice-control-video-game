import pygame as pg

from app.background import get_random_background
from app.base.game_object import GameObject
from app.base.scene import Scene


class BeautyScene(Scene):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()
        self._cursor_group = pg.sprite.Group()

        pg.mouse.set_visible(False)
        self._cursor = GameObject("cursor", (0, 0), (20, 20), self._cursor_group,
                                  image=pg.image.load("Assets/Images/TargetMask.png"), background="white")

        self._bg = get_random_background("Assets/Images/TailMaps/GrassTileset.png", (w, h), (32, 32))


    def draw(self):
        super().draw()
        self._cursor_group.draw(self)

    def draw_background(self):
        self.blit(self._bg, (0, 0))

    def update(self):
        self._cursor.rect.center = pg.mouse.get_pos()
