from threading import Thread

import pygame as pg

from app import consts
from app.base.translator import tr
from app.controllers.attack import MagicController
from app.voice.voice_recognizer import RealTimeCommandRecognizer


class VoiceMagicController(MagicController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__recognizer = RealTimeCommandRecognizer(
            tr(list(consts.SPELLS)),
            on_detected=self.__on_detected)

        self.__thread = Thread(target=self.__recognizer.run)
        self.__thread.start()
        self.__closed = False
        self.__voice_state = self._state

    def __on_detected(self, word):
        for key, spell in self._spells.items():
            if word in spell.activate_words:
                self.__voice_state = key

    def attack(self):
        self._state = self.__voice_state
        self.__voice_state = consts.IDLE

        self._attack_event(self._state, pg.mouse.get_pos())

    def close(self):
        self.__closed = True
        self.__recognizer.close()
        self.__thread.join()
