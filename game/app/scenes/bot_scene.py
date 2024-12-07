import pygame as pg

from app.scenes.game_scene import GameScene


class BotScene(GameScene):
    __key__ = "Bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self):
        super().draw()

    def update(self):
        super().update()

    def close(self):
        super().close()
