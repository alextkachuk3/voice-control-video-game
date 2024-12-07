import random as rd
from datetime import datetime

import pygame as pg
import pyperclip

from app.base.scene import SceneController
from app.base.storage import Storage
from app.base.ui import TextField, Button, Label, ImageButton
from app.consts import WIDTH, HEIGHT
from app.network.db import database
from app.players.player_factory import PlayerFactory
from app.scenes.beauty_scene import BeautyScene
from app.scenes.statement import PlayerStatement
from app.thread_contoller import ThreadController
from app.utility import generate_nickname


class LobbyScene(BeautyScene):
    __key__ = "Lobby"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.create_btn = Button((100, 40), (w // 2, h // 2 - 45), self._ui_group,
                                 text="Create room", bg_color="green", on_clicked=self.__on_create)

        self.join_btn = Button((100, 40), (w // 2, h // 2 + 45), self._ui_group,
                               text="Join room", bg_color="yellow", on_clicked=self.__on_join)

        Storage.set("nickname", generate_nickname())

    def __create_room(self):
        player = Storage.get("player")
        nickname = Storage.get("nickname", "host")

        response = database().child("rooms").push(
            {
                "created": str(datetime.now()),
                "players": {
                    "host": {
                        "nickname": nickname,
                        "ready": False,
                        "character": player
                    }
                }
            })

        code = response["name"]
        Storage.set("code", code)
        Storage.set("id", "host")

    def __on_create(self):
        self.__create_room()
        Storage.set("role", "host")
        SceneController.open_scene("WaitRoom", False, self.get_size())

    def __on_join(self):
        Storage.set("role", "guest")
        SceneController.open_scene("Code", False, self.get_size())


class WaitRoomScene(BeautyScene):
    __key__ = "WaitRoom"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.role = Storage.get("role")
        self.code = Storage.get("code")
        pyperclip.copy(self.code)

        role = Storage.get("role")

        label = Label((300, 30), (w // 2, h // 2 - 90), self._ui_group,
                      text="Code copied! Send it to friend" if role == "host" else "You joined!")
        label = Label((300, 30), (w // 2, h // 2 - 45), self._ui_group, text=self.code)
        copy_btn = ImageButton((25, 25), (0, h // 2 - 45), self._ui_group,
                               picture=pg.image.load("Assets/Images/Paste.png"),
                               on_clicked=self.__on_copy)

        copy_btn.rect.left = label.rect.right + 5

        self.ready_btn = Button((100, 40), (w // 2, h // 2 + 45), self._ui_group,
                                text="Ready", bg_color="red", on_clicked=self.__on_ready)

        self.ready = False

        self.host_statement = None
        self.guest_statement = None
        self.font = pg.font.Font(None, 20)
        self.id = Storage.get("id")
        self.players = {}

        self.connect_stream = database().child("rooms").child(self.code).stream(self.__on_connected)

        self.start_btn = None

        if role == "host":
            self.start_btn = Button((100, 40), (w // 2, h // 2 + 95), self._ui_group,
                                    text="Start", bg_color="yellow", on_clicked=self.__on_go)

    def __on_copy(self):
        pyperclip.copy(self.code)

    def draw(self):
        super().draw()
        if self.start_btn is None:
            return
        self.start_btn.enabled = False

        for _, player in self.players.items():
            if not player["value"]["ready"]:
                break
        else:
            self.start_btn.enabled = True

    def __get_free_space(self, x, y, w, h):
        for item in self._ui_group:
            if item.rect.colliderect(pg.rect.Rect(x, y, w, h)):
                x = rd.randint(w, WIDTH - w)
                y = rd.randint(h, HEIGHT - h)

        return x, y

    def __update_player(self, name, value_map):
        if name not in self.players:
            return
        player = self.players[name]
        for key, value in value_map.items():
            if key in player["value"]:
                player["value"][key] = value

        player["statement"].color = "green" if player["value"]["ready"] else "red"

    def __add_player(self, key, value):
        if key in self.players:
            instance = self.players[key]
            instance["value"] = value
            self.__update_player(key, {})
            return

        player = PlayerFactory.spawn(value["character"], (0, 0), (100, 100))

        x, y = self.__get_free_space(50, 50, 100, 100)
        statement = PlayerStatement((x, y), self._ui_group, player, value["nickname"], self.font)
        self.players[key] = {"value": value, "statement": statement}
        self.__update_player(key, {})

    def __on_connected(self, message):
        if message["event"] not in ["put", "patch"]:
            return

        print(message)
        players = None
        path = message["path"]

        if path == "/" and message["data"] is None:
            ThreadController.run_on_main(SceneController.open_scene, "Main", True, self.get_size())
            return

        if path == "/go" and message["data"]:
            self.__start_game()
            return

        if path == "/":
            players = message["data"]["players"]
        elif path == "/players":
            players = message["data"]
        elif path.startswith("/players/") and path.endswith("/ready"):
            key = path[len("/players/"):-len("/ready")]
            self.__update_player(key, {"ready": message["data"]})
        elif path.startswith("/players/") and message["data"] is not None:
            self.__add_player(path[len("/players/"):], message["data"])

        elif message["data"] is None:
            for player in list(self.players.keys()):
                if player in path:
                    self.players[player]["statement"].kill()
                    del self.players[player]

        if not isinstance(players, dict):
            return

        for player, value in players.items():
            if isinstance(value, dict):
                self.__add_player(player, value)

        if path != "/":
            return

        for player in list(self.players.keys()):
            if player not in players:
                self.players[player]["statement"].kill()
                del self.players[player]

    def __start_game(self):
        data = {key: player["value"] for key, player in self.players.items()}
        Storage.set("players", data)
        ThreadController.run_on_main(SceneController.open_scene, "Online", True, self.get_size())

    def __on_ready(self):
        self.ready = not self.ready
        self.ready_btn.bg_color = "green" if self.ready else "red"
        database().child("rooms").child(self.code).child("players").child(self.id) \
            .child("ready").set(self.ready)

    def __on_go(self):
        database().child("rooms").child(self.code).child("go").set(True)

    def _on_back(self):
        super()._on_back()

    def update(self):
        super().update()

    def close(self):
        super().close()
        try:
            self.connect_stream.close()
        except:
            pass

        database().child("rooms").child(self.code).child("players").child(self.id).remove()
        if self.id == "host":
            database().child("rooms").child(self.code).remove()


class CodeScene(BeautyScene):
    __key__ = "Code"
    __caption__ = "Join to room"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.__code_field = TextField((w // 2, 60), (w // 2, h // 2), self._ui_group)
        paste_btn = ImageButton((50, 50), (0, h // 2), self._ui_group,
                                picture=pg.image.load("Assets/Images/Paste.png"),
                                on_clicked=self.__on_paste)

        paste_btn.rect.left = self.__code_field.rect.right + 5

        ok_btn = Button((80, 40), (w // 2, h // 2 + 100), self._ui_group, text="Ok", bg_color="green",
                        on_clicked=self.__on_ok)

    def __on_paste(self):
        self.__code_field.text = pyperclip.paste()

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pg.KEYDOWN and event.unicode == "\x16":
            self.__code_field.text = pyperclip.paste()
            return

        self.__code_field.type(event)

    def __on_ok(self):
        text = self.__code_field.text
        if len(text) == 0:
            return

        data = database().child("rooms").child(text).get().val()
        if data is None:
            self.__code_field.color = "red"
            self.__code_field.text = "Invalid"
            return
        self.__code_field.text = ""
        self.__code_field.color = "black"

        Storage.set("code", text)
        player = Storage.get("player")
        nickname = Storage.get("nickname", "guest")
        response = database().child("rooms").child(text).child("players").push({
            "nickname": nickname,
            "character": player,
            "ready": False
        })
        Storage.set("id", response["name"])

        SceneController.open_scene("WaitRoom", True, self.get_size())

    def update(self):
        super().update()
        self._ui_group.update()
