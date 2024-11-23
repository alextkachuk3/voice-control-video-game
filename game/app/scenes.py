import pygame as pg

from app.base.animator import Animation
from app.player_animator import get_player_animator, get_animator_controller
from app.base.scene import Scene, SceneController
from app.base.ui import Button
from app.player import Player, KeyboardPlayer


class MainScene(Scene):
    __title__ = "MainScene"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.start_btn = Button((100, 40), (w // 2, h // 2), self._draw_group,
                                label="Start", bg_color="green")

        self.quit_btn = Button((100, 40), (w // 2, 0), self._draw_group,
                               label="Quit", bg_color="tomato")

        self.quit_btn.rect.top = self.start_btn.rect.bottom + 10



    def draw_background(self):
        self.fill("white")


    def update(self):
        if self.start_btn.is_clicked():
            SceneController.open_scene("Level2", False, self.get_size())
        if self.quit_btn.is_clicked():
            SceneController.is_running = False



class Level2(Scene):
    __title__ = "Level2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()

        self.player_group = pg.sprite.Group()
        animator_controller = get_animator_controller((48, 48), "Assets/Images/Characters/Necromancer")
        self.player = KeyboardPlayer((w // 2, h // 2), (100, 100), self.player_group, 2, animator_controller)

    def draw(self):
        super().draw()
        self.player_group.draw(self)
    def draw_background(self):
        self.fill("white")
    def update(self):
        self.player_group.update()

        self._clock.tick(60)
