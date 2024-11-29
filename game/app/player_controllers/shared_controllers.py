from threading import Thread

import pygame as pg

from app import consts
from app.controllers.attack import MagicController
from app.controllers.move import MoveController

class DelegatingMeta(type):
    def __new__(cls, name, bases, attrs):
        for base_class in bases:
            if base_class is object:
                continue

            for attr_name in dir(base_class):
                if (not attr_name.startswith("_") and callable(getattr(base_class, attr_name))
                        and attr_name not in attrs):
                    attrs[attr_name] = cls.create_delegate(attr_name)

        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def create_delegate(attr_name):
        def method(self, *args, **kwargs):
            if self._controller and hasattr(self._controller, attr_name):
                return getattr(self._controller, attr_name)(*args, **kwargs)

            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr_name}'")

        return method


class SharedMoveController(MoveController, metaclass=DelegatingMeta):
    def __init__(self, controller:MoveController, database_getter=None):
        super().__init__(controller.owner, controller.state, controller.side, controller.speed)

        self._controller = controller
        self.__database_getter = database_getter

    def __update(self):
        if self.__database_getter is None:
            return
        try:
            self.__database_getter().child("move").set({
                "x":self._controller.owner.rect.centerx,
                "y":self._controller.owner.rect.centery,
                "side": self._controller.side,
                "state": self._controller.state
            })
        except:
            pass

    def move(self):
        if self._controller.state not in [consts.IDLE, consts.RUN]:
            return

        self._controller.move()

        thread = Thread(target=self.__update)
        thread.start()


class SharedMagicController(MagicController, metaclass=DelegatingMeta):
    def __init__(self, controller:MagicController, database_getter=None):
        super().__init__(controller.owner, controller.state)

        self._controller = controller
        self.__database_getter = database_getter

    def __update(self):
        if self.__database_getter is None:
            return
        try:
            self.__database_getter().child("attack").set({
                "state": self._controller.state,
                "mousex": pg.mouse.get_pos()[0],
                "mousey": pg.mouse.get_pos()[1],
            })
        except:
            pass

    def attack(self):
        if self._controller.state not in [consts.IDLE, consts.RUN]:
            return
        self._controller.attack()

        thread = Thread(target=self.__update)
        thread.start()
