import pygame as pg

from app.base.scene import SceneController
from app.base.ui import ImageButton
from app.scenes.beauty_scene import BeautyScene
from app.base.storage import Storage
from app.keyboard_controllers import KeyboardMoveController, KeyboardMagicController
from app.players.player_factory import PlayerFactory


class GameScene(BeautyScene):
    __title__ = "Game"
    DEBUG=True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()


        self._back_btn = ImageButton((50, 50), (0, 0), self._draw_group,
                                     image=pg.image.load("Assets/Images/Back.png"))
        self._back_btn.rect.topleft = 5, 5
        self._player_group = pg.sprite.Group()
        self._spell_group = pg.sprite.Group()

        player = Storage.get("player")
        self.DEBUG = Storage.get("debug", True)

        self._player = None

        if player:
            self._player = PlayerFactory.spawn(player, (w // 2, h // 2), (100, 100), self._player_group, self._draw_group,
                                               spell_groups=(self._spell_group, self._draw_group))

            self._player.set_move_controller(KeyboardMoveController(self._player.rect, speed=2))
            self._player.set_attack_controller(KeyboardMagicController(self._player.rect, owner=self._player))


    def draw(self):
        super().draw()
        if self.DEBUG:
            for obj in self._draw_group:
                pg.draw.rect(self, "black",obj.bounding_rect, width=1)

            for player in self._player_group:
                pg.draw.circle(self, "black", player.rect.center, radius=150, width=1)


    def update(self):
        super().update()

        self._player_group.update()
        self._spell_group.update(self._player_group)

        if self._back_btn.is_clicked():
            SceneController.open_scene("Main", close_prev=True)
