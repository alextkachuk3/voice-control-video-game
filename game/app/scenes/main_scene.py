from app.background import get_random_background
from app.base.scene import Scene, SceneController
from app.base.ui import Button


class MainScene(Scene):
    __title__ = "MainScene"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()
        self.bg = get_random_background("Assets/Images/TailMaps/Dungeon_Tileset.png", (w, h),
                                        (16, 16))

        self.start_btn = Button((100, 40), (w // 2, h // 2), self._draw_group,
                                label="Start", bg_color="green")

        self.quit_btn = Button((100, 40), (w // 2, 0), self._draw_group,
                               label="Quit", bg_color="tomato")

        self.quit_btn.rect.top = self.start_btn.rect.bottom + 10



    def draw_background(self):
        self.blit(self.bg, (0, 0))


    def update(self):
        if self.start_btn.is_clicked():
            SceneController.open_scene("GameScene", False, self.get_size())
        if self.quit_btn.is_clicked():
            SceneController.is_running = False