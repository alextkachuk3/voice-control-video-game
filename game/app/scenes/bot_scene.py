import pygame as pg

from app.scenes.game_scene import GameScene

from app.players.player_factory import PlayerFactory


class BotScene(GameScene):
    __key__ = "Bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self._player = PlayerFactory.spawn("Sorceress", (w // 2, h // 2), (100, 100), self._player_group,
                                           self._draw_group,
                                           spell_groups=(self._spell_group, self._draw_group), hp=100)

    def draw(self):
        super().draw()

    def update(self):
        super().update()

    def close(self):
        super().close()
