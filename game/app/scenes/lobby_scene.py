from datetime import datetime
import random as rd

import pyperclip
import pygame as pg

from app.base.scene import SceneController
from app.base.storage import Storage
from app.base.ui import TextField, Button, Label
from app.consts import WIDTH, HEIGHT
from app.network.db import database
from app.players.player_factory import PlayerFactory
from app.scenes.beauty_scene import BeautyScene
from app.scenes.statement import PlayerStatement


class LobbyScene(BeautyScene):
    __title__ = "Lobby"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.create_btn = Button((100, 40), (w//2, h//2-45), self._ui_group,
                                 text="Create room", bg_color="green")

        self.join_btn = Button((100, 40), (w // 2, h//2+45), self._ui_group,
                               text="Join room", bg_color="yellow")

    def create_room(self):
        player = Storage.get("player")
        nickname = Storage.get("nickname", "host")

        response = database.child("rooms").push(
            {
                "created":str(datetime.now()),
                "players":{
                    "host":{
                        "nickname":nickname,
                        "ready": False,
                        "character": player
                    }
                }
            })

        code = response["name"]
        Storage.set("code", code)
        Storage.set("id", "host")


    def update(self):
        super().update()

        if self.create_btn.is_clicked():
            self.create_room()
            Storage.set("role", "host")
            SceneController.open_scene("WaitRoom", False, self.get_size())
        elif self.join_btn.is_clicked():
            Storage.set("role", "guest")
            SceneController.open_scene("Code", False, self.get_size())

class WaitRoomScene(BeautyScene):
    __title__ = "WaitRoom"
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

        self.ready_btn = Button((100, 40), (w // 2, h // 2 + 45), self._ui_group,
                                text="Ready", bg_color="red")

        self.ready = False

        self.host_statement = None
        self.guest_statement = None
        self.font = pg.font.Font(None, 20)
        self.id = Storage.get("id")
        self.players = {}

        self.connect_stream =database.child("rooms").child(self.code).stream(self._on_connected)
        print(self.code)

    def get_free_space(self, x, y, w, h):
        for item in self._ui_group:
            if item.rect.colliderect(pg.rect.Rect(x, y, w, h)):
                x = rd.randint(w, WIDTH-w)
                y = rd.randint(h, HEIGHT-h)

        return x, y

    def add_player(self, key, value):
        self.players[key] = value
        player = PlayerFactory.spawn(value["character"], (0, 0), (100, 100))

        x, y = self.get_free_space(50, 50, 100, 100)
        statement = PlayerStatement((x, y), self._ui_group, player, value["nickname"], self.font)

        value["statement"] = statement

    def _on_connected(self, message):
        print("connected", message)

        if message["event"] not in ["put", "patch"]:
            return

        players = None
        path = message["path"]
        if "/" == path:
            players = message["data"]["players"]
        elif "/players" == path:
            players = message["data"]
        elif message["data"] is None:
            for player in list(self.players.keys()):
                if player in path:
                    self.players[player]["statement"].kill()
                    del self.players[player]

        if not isinstance(players, dict):
            return

        for player, value in players.items():
            if player not in self.players and isinstance(value, dict):
                self.add_player(player, value)

        if path != "/":
            return

        for player in list(self.players.keys()):
            if player not in players:
                self.players[player]["statement"].kill()
                del self.players[player]


    def update(self):
        super().update()

        if self.ready_btn.is_clicked():
            self.ready = not self.ready
            self.ready_btn.bg_color = "green" if self.ready else "red"
            database.child("rooms").child(self.code).child("players").child(self.id)\
                .child("ready").set(self.ready)

    def close(self):
        super().close()
        print("close")
        try:
            self.connect_stream.close()
        except:
            pass

class CodeScene(BeautyScene):
    __title__ = "Code"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        self.code_field = TextField((w//2, 60), (w//2, h//2), self._ui_group)
        self.code_field.text = pyperclip.paste()

        self.ok_btn = Button((80, 40), (w//2, h//2+65), self._ui_group, text="Ok", bg_color="green")

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pg.KEYDOWN and event.unicode == "\x16":
            self.code_field.text = pyperclip.paste()
            return

        self.code_field.type(event)

    def update(self):
        super().update()
        self._ui_group.update()

        text = self.code_field.text
        if self.ok_btn.is_clicked() and len(text) > 0:
            data = database.child("rooms").child(text).get().val()
            if data is None:
                self.code_field.color = "red"
                self.code_field.text = "Invalid"
                return
            self.code_field.text = ""
            self.code_field.color = "black"

            Storage.set("code", text)
            player = Storage.get("player")
            nickname = Storage.get("nickname", "guest")
            response = database.child("rooms").child(text).child("players").push({
                "nickname": nickname,
                "character": player,
                "ready": False
            })
            Storage.set("id", response["name"])

            SceneController.open_scene("WaitRoom", True, self.get_size())
