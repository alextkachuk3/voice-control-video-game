from threading import Thread

import pygame as pg

from app import consts
from app.controllers.attack import MagicController
from app.controllers.move import MoveController


class SharedMoveController(MoveController):
    def __init__(self, controller:MoveController, database_getter=None):
        super().__init__(controller.owner, controller.state, controller.side, controller.speed)

        self.__controller = controller
        self.__database_getter = database_getter

    def __update(self):
        if self.__database_getter is None:
            return
        try:
            self.__database_getter().child("move").set({
                "x":self.__controller.owner.rect.centerx,
                "y":self.__controller.owner.rect.centery,
                "side": self.__controller.side,
                "state": self.__controller.state
            })
        except:
            pass

    def move(self):
        if self.__controller.state not in [consts.IDLE, consts.RUN]:
            return

        self.__controller.move()

        thread = Thread(target=self.__update)
        thread.start()

    def set_state(self, state):
        self.__controller.set_state(state)

    def set_side(self, side):
        self.__controller.set_side(side)

    def subscribe_on_success(self, callback):
        self.__controller.subscribe_on_success(callback)

    def unsubscribe_on_success(self, callback):
        self.__controller.unsubscribe_on_success(callback)


class SharedMagicController(MagicController):
    def __init__(self, controller:MagicController, database_getter=None):
        super().__init__(controller.owner, controller.state)

        self.__controller = controller
        self.__database_getter = database_getter

    def __update(self):
        if self.__database_getter is None:
            return
        try:
            self.__database_getter().child("attack").set({
                "state": self.__controller.state,
                "mousex": pg.mouse.get_pos()[0],
                "mousey": pg.mouse.get_pos()[1],
            })
        except:
            pass

    def add_spell(self, key, spell_spawner):
        self.__controller.add_spell(key, spell_spawner)

    def attack(self):
        if self.__controller.state not in [consts.IDLE, consts.RUN]:
            return
        self.__controller.attack()

        thread = Thread(target=self.__update)
        thread.start()

    def set_state(self, state):
        self.__controller.set_state(state)

    def subscribe_on_success(self, callback):
        self.__controller.subscribe_on_success(callback)

    def unsubscribe_on_success(self, callback):
        self.__controller.unsubscribe_on_success(callback)
