from threading import Thread

import pygame as pg

from app import consts
from app.player_controllers.keyboard_controllers import KeyboardMoveController, KeyboardMagicController


class SharedMoveController(KeyboardMoveController):
    def __init__(self, owner, default_state=consts.IDLE, default_side=pg.K_a, speed=0, database_getter=None):
        super().__init__(owner, default_state, default_side, speed)

        self.__database_getter = database_getter

    def __update(self):
        if self.__database_getter is None:
            return
        try:
            self.__database_getter().child("move").set({
                "x":self._owner.rect.centerx,
                "y":self._owner.rect.centery,
                "side": self._side,
                "state": self._state
            })
        except:
            pass

    def move(self):
        if self._state not in [consts.IDLE, consts.RUN]:
            return

        super().move()

        thread = Thread(target=self.__update)
        thread.start()

class SharedMagicController(KeyboardMagicController):
    def __init__(self, *args, database_getter=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.__database_getter = database_getter
    def __update(self):
        if self.__database_getter is None:
            return
        try:
            self.__database_getter().child("attack").set({
                "state": self._state,
                "mousex": pg.mouse.get_pos()[0],
                "mousey": pg.mouse.get_pos()[1],
            })
        except:
            pass

    def attack(self):
        if self._state not in [consts.IDLE, consts.RUN]:
            return
        super().attack()

        thread = Thread(target=self.__update)
        thread.start()
