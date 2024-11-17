import pygame as pg

from app.scene import Scene, SceneController
from app.ui import Button


class MainScene(Scene):
    __title__ = "MainScene"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.start_btn = Button((100, 40), (w//2, h//2), self._draw_group,
                                label="Start", bg_color="green")

        self.quit_btn = Button((100, 40), (w//2, 0), self._draw_group,
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

        self.rect = pg.Rect(100, 100, 50, 50)

    def draw(self):
        self.fill("white")
        pg.draw.rect(self, "red", self.rect)

    def update(self):
        self._clock.tick(60)

        self.rect.y += 1

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN:
            SceneController.open_scene("MainScene", False, self.get_size())