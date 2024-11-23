import os.path

import pygame as pg

from app.background import get_random_background
from app.base.scene import Scene
from app.base.tail_map_builder import TailMapBuilder
from app.player import KeyboardPlayer
from app.player_animator import get_animator_controller


class GameScene(Scene):
    __title__ = "GameScene"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()

        self.player_group = pg.sprite.Group()
        animator_controller = get_animator_controller((48, 48), "Assets/Images/Characters/Necromancer")
        self.player = KeyboardPlayer((w // 2, h // 2), (100, 100), self.player_group, 2, animator_controller)

        self.bg = get_random_background("Assets/Images/TailMaps/TX Tileset Grass.png", (w, h), (32, 32))


    def draw(self):
        super().draw()
        self.player_group.draw(self)
    def draw_background(self):
       self.blit(self.bg, (0, 0))

    def update(self):
        self.player_group.update()

        self._clock.tick(60)
