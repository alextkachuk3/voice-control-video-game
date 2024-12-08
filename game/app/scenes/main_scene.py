from app.background import get_random_background
from app.base.scene import Scene, SceneController
from app.base.storage import Storage
from app.base.translator import tr
from app.base.ui import Button


class MainScene(Scene):
    __key__ = "Main"
    __caption__ = "Voice control video game"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()
        self.bg = get_random_background("Assets/Images/TailMaps/DungeonTileset.png", (w, h),
                                        (16, 16))

        self.online_btn = Button((120, 40), (w // 2, h // 2.6), self._ui_group,
                                 text=tr("online"), bg_color="green", on_clicked=self.__on_online)

        self.bot_btn = Button((120, 40), (w // 2, 0), self._ui_group,
                                text=tr("bot"), bg_color="palegreen2", on_clicked=self.__on_bot)

        self.bot_btn.rect.top = self.online_btn.rect.bottom + 10

        self.train_btn = Button((120, 40), (w // 2, 0), self._ui_group,
                                text=tr("training"), bg_color="yellow", on_clicked=self.__on_train)

        self.train_btn.rect.top = self.bot_btn.rect.bottom + 10

        self.help_btn = Button((120, 40), (w // 2, 0), self._ui_group,
                                text=tr("help"), bg_color="purple", on_clicked=self.__on_help)

        self.help_btn.rect.top = self.train_btn.rect.bottom + 10

        self.quit_btn = Button((120, 40), (w // 2, 0), self._ui_group,
                               text=tr("quit"), bg_color="tomato", on_clicked=self.__on_quit)

        self.quit_btn.rect.top = self.help_btn.rect.bottom + 10

    def draw_background(self):
        self.blit(self.bg, (0, 0))

    def __on_online(self):
        Storage.set("prev", "Main")
        Storage.set("nextscene", "Lobby")
        SceneController.open_scene("Selection", False, self.get_size())

    def __on_bot(self):
        Storage.set("prev", "Main")
        Storage.set("nextscene", "Bot")
        SceneController.open_scene("Selection", True, self.get_size())

    def __on_train(self):
        Storage.set("nextscene", "Training")
        Storage.set("prev", "Main")
        SceneController.open_scene("Selection", False, self.get_size())

    def __on_help(self):
        Storage.set("nextscene", "Help")
        Storage.set("prev", "Main")
        SceneController.open_scene("Help", False, self.get_size())

    def __on_quit(self):
        SceneController.is_running = False
