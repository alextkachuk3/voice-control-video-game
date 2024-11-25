from app.base.scene import SceneController
from app.base.storage import Storage
from app.base.ui import TextField, Button
from app.scenes.beauty_scene import BeautyScene


class LobbyScene(BeautyScene):
    __title__ = "Lobby"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.create_btn = Button((100, 40), (w//2, h//2), self._ui_group,
                                 label="Create room", bg_color="green")

        self.join_btn = Button((100, 40), (w // 2, h//2+45), self._ui_group,
                               label="Join room", bg_color="yellow")


    def update(self):
        super().update()

        if self.create_btn.is_clicked():
            pass
        elif self.join_btn.is_clicked():
            Storage.set("prev", "Lobby")
            SceneController.open_scene("Code", False, self.get_size())

class CodeScene(BeautyScene):
    __title__ = "Code"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.code_field = TextField((w//2, 60), (w//2, h//2), self._ui_group)

        self.ok_btn = Button((80, 40), (w//2, h//2+65), self._ui_group, label="Ok", bg_color="green")

    def handle_event(self, event):
        super().handle_event(event)
        self.code_field.type(event)

    def update(self):
        super().update()

        self._ui_group.update()

