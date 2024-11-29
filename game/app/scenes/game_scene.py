import pygame as pg

from app import consts
from app.player_controllers.shared_controllers import SharedMoveController, SharedMagicController
from app.player_controllers.voice_controllers import VoiceMagicController
from app.scenes.beauty_scene import BeautyScene
from app.base.storage import Storage
from app.player_controllers.keyboard_controllers import KeyboardMoveController, KeyboardMagicController
from app.players.player_factory import PlayerFactory


class GameScene(BeautyScene):
    __key__ = "Game"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()

        self._player_group = pg.sprite.Group()
        self._spell_group = pg.sprite.Group()

        player = Storage.get("player")

        self._player = None

        if player:
            self._player = PlayerFactory.spawn(player, (w // 2, h // 2), (100, 100), self._player_group,
                                               self._draw_group,
                                               spell_groups=(self._spell_group, self._draw_group), hp=100)

            self._player.set_move_controller(KeyboardMoveController(self._player, speed=2))
            self._player.set_attack_controller(VoiceMagicController(self._player))


    def draw(self):
        super().draw()
        if consts.DEBUG:
            for obj in self._draw_group:
                pg.draw.rect(self, "black",obj.bounding_rect, width=1)

            for player in self._player_group:
                pg.draw.circle(self, "black", player.rect.center, radius=150, width=1)


    def update(self):
        super().update()

        self._player_group.update()
        self._spell_group.update(self._player_group)

    def close(self):
        super().close()
        self._player.close_controllers()
