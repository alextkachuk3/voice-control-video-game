from app.background import get_random_background
from app.base.scene import Scene, SceneController
from app.base.storage import Storage
from app.base.ui import Button


class MainScene(Scene):
    __title__ = "Main"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()
        self.bg = get_random_background("Assets/Images/TailMaps/DungeonTileset.png", (w, h),
                                        (16, 16))

        self.online_btn = Button((100, 40), (w // 2, h // 2), self._ui_group,
                                text="Online", bg_color="green")

        self.train_btn = Button((100, 40), (w // 2, 0), self._ui_group,
                                text="Training", bg_color="yellow")

        self.train_btn.rect.top = self.online_btn.rect.bottom + 10

        self.quit_btn = Button((100, 40), (w // 2, 0), self._ui_group,
                               text="Quit", bg_color="tomato")

        self.quit_btn.rect.top = self.train_btn.rect.bottom + 10



    def draw_background(self):
        self.blit(self.bg, (0, 0))


    def update(self):
        super().update()

        if self.online_btn.is_clicked():
            Storage.set("prev", "Main")
            Storage.set("nextscene", "Lobby")
            SceneController.open_scene("Selection", False, self.get_size())

        if self.train_btn.is_clicked():
            Storage.set("nextscene", "Training")
            Storage.set("prev", "Main")
            SceneController.open_scene("Selection", False, self.get_size())

        if self.quit_btn.is_clicked():
            SceneController.is_running = False