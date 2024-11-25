import pygame as pg

from app.background import get_random_background
from app.base.game_object import GameObject
from app.base.scene import Scene, SceneController
from app.base.storage import Storage
from app.base.ui import ImageButton


class BeautyScene(Scene):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()
        self._cursor_group = pg.sprite.Group()

        pg.mouse.set_visible(False)
        self._cursor = GameObject("cursor", (0, 0), (20, 20), self._cursor_group,
                                  image=pg.image.load("Assets/Images/TargetMask.png"), background="white")

        self._back_btn = ImageButton((50, 50), (0, 0), self._ui_group,
                                     image=pg.image.load("Assets/Images/Back.png"))
        self._back_btn.rect.topleft = 5, 5

        self._bg = get_random_background("Assets/Images/TailMaps/GrassTileset.png", (w, h), (32, 32))


    def draw(self):
        super().draw()
        self._cursor_group.draw(self)

    def draw_background(self):
        self.blit(self._bg, (0, 0))

    def update(self):
        self._cursor.rect.center = pg.mouse.get_pos()

        if self._back_btn.is_clicked():
            SceneController.open_scene(Storage.get("prev", "Main"), True, self.get_size())
