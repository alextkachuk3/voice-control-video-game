from app.base.storage import Storage
from app.consts import WIDTH, HEIGHT
from app.keyboard_controllers import KeyboardMoveController, KeyboardMagicController
from app.players.player_factory import PlayerFactory
from app.scenes.beauty_scene import BeautyScene

import pygame as pg
import random as rd

class OnlineScene(BeautyScene):
    __title__ = "Online"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        players = Storage.get("players")
        owner_nickname = Storage.get("nickname")

        self._players = {}
        self._player_group = pg.sprite.Group()
        self._spell_group = pg.sprite.Group()

        w, h = self.get_size()
        print(owner_nickname)
        for _, player in players.items():
            instance = PlayerFactory.spawn(player["character"], self.get_free_space(w//2, h//2, 100, 100),
                                (100, 100), self._player_group, self._draw_group,
                                spell_groups=(self._spell_group, self._draw_group))
            if player["nickname"] == owner_nickname:
                instance.set_move_controller(KeyboardMoveController(instance.rect, speed=2))
                instance.set_attack_controller(KeyboardMagicController(instance.rect, owner=instance))


    def get_free_space(self, x, y, w, h):
        for item in self._ui_group:
            if item.rect.colliderect(pg.rect.Rect(x, y, w, h)):
                x = rd.randint(w, WIDTH-w)
                y = rd.randint(h, HEIGHT-h)

        return x, y

    def update(self):
        super().update()

        self._player_group.update()
        self._spell_group.update(self._player_group)
