import pygame as pg

from app.base.storage import Storage
from app.network.db import database
from app.player_controllers.keyboard_controllers import KeyboardMoveController
from app.player_controllers.network_controllers import NetworkMoveController, NetworkMagicController
from app.player_controllers.shared_controllers import SharedMoveController, SharedMagicController
from app.player_controllers.voice_controllers import VoiceMagicController
from app.players.player_factory import PlayerFactory
from app.scenes.beauty_scene import BeautyScene


class OnlineScene(BeautyScene):
    __key__ = "Online"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        players = Storage.get("players")
        owner_nickname = Storage.get("nickname")
        self.code = Storage.get("code")

        self._players = {}
        self._player_group = pg.sprite.Group()
        self._spell_group = pg.sprite.Group()

        w, h = self.get_size()
        print(owner_nickname)
        for pid, player in players.items():
            instance = PlayerFactory.spawn(player["character"], (w // 2, h // 2),
                                           (100, 100), self._player_group, self._draw_group,
                                           spell_groups=(self._spell_group, self._draw_group), hp=100)

            database_getter = lambda id=pid: (database().child("rooms").child(self.code).child("players").child(id)
                                              .child("controllers"))
            if player["nickname"] == owner_nickname:
                move = SharedMoveController(KeyboardMoveController(instance, speed=2), database_getter=database_getter)
                attack = SharedMagicController(VoiceMagicController(instance), database_getter=database_getter)
            else:
                move = NetworkMoveController(instance, speed=2, database_ref=database_getter())
                attack = NetworkMagicController(instance, database_ref=database_getter())

            instance.set_move_controller(move)
            instance.set_attack_controller(attack)

    def update(self):
        super().update()

        self._player_group.update()
        self._spell_group.update(self._player_group)

    def close(self):
        super().close()

        for player in self._player_group:
            player.close_controllers()
