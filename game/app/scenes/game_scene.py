import pygame as pg

from app.background import get_random_background
from app.base.game_object import GameObject
from app.base.scene import Scene
from app.keyboard_controllers import KeyboardMoveController, KeyboardMagicController
from app.players.player_factory import PlayerFactory


class GameScene(Scene):
    __title__ = "Game"
    DEBUG=True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()

        self.player_group = pg.sprite.Group()
        self.spell_group = pg.sprite.Group()

        pg.mouse.set_visible(False)
        self.cursor = GameObject("cursor", (0, 0), (20, 20), self._draw_group,
                                 image=pg.image.load("Assets/Images/target-mask.png"), background="white")

        self.player = PlayerFactory.spawn("Cultist", (w // 2, h // 2), (100, 100), self.player_group, self._draw_group,
                                    spell_groups=(self.spell_group, self._draw_group))

        self.player.set_move_controller(KeyboardMoveController(self.player.rect,speed=2))
        self.player.set_attack_controller(KeyboardMagicController(self.player.rect, owner=self.player))

        self.bg = get_random_background("Assets/Images/TailMaps/GrassTileset.png", (w, h), (32, 32))


    def draw(self):
        super().draw()
        if self.DEBUG:
            for obj in self._draw_group:
                pg.draw.rect(self, "black",obj.bounding_rect, width=1)
            pg.draw.circle(self, "black", self.player.rect.center, radius=150, width=1)
    def draw_background(self):
       self.blit(self.bg, (0, 0))

    def update(self):
        self.cursor.rect.center = pg.mouse.get_pos()

        self.player_group.update()
        self.spell_group.update(self.player_group)

        self._clock.tick(60)
