from threading import Thread

import pygame as pg

from app import consts
from app.controllers.attack import MagicController
from app.voice.voice_recognizer import RealTimeCommandRecognizer


class VoiceMagicController(MagicController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__recognizer = RealTimeCommandRecognizer(
            ["вогняна куля", "морозна піка", "тайфун", "відкладений вибух", "покласти міну",
             "кровава баня", "земляний спис", "токсична хмара"],
                                                      on_detected=self.__on_detected)

        self.__thread = Thread(target=self.__recognizer.run)
        self.__thread.start()
        self.__closed = False
        self.__voice_state = self._state

    def __on_detected(self, word):
        if word in ["вогняна куля", "кровава баня"]:
            self.__voice_state = consts.ATTACK1
        elif word in ["морозна піка", "відкладений вибух", "земляний спис"]:
            self.__voice_state = consts.ATTACK2
        elif word in ["тайфун", "покласти міну", "токсична хмара"]:
            self.__voice_state = consts.ATTACK3


    def attack(self):
        self._state = self.__voice_state
        self.__voice_state = consts.IDLE

        self._attack_event(self._state, pg.mouse.get_pos())

    def close(self):
        self.__closed = True
        self.__recognizer.close()
        self.__thread.join()
