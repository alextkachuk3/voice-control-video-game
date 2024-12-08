import pygame as pg
from app.controllers.move import MoveController
from app.controllers.attack import MagicController
from app import consts
import random


class BotMoveController(MoveController):
    def __init__(self, bot, player, default_state=consts.IDLE, speed=1):
        super().__init__(bot, default_state, pg.K_a, speed)
        self._player = player

    def move(self):
        if not self._player.alive():
            self._state = consts.IDLE
            return

        bot_pos = pg.math.Vector2(self._owner.rect.center)
        player_pos = pg.math.Vector2(self._player.rect.center)

        direction = player_pos - bot_pos

        if direction.x == 0 and direction.y == 0:
            return
        else:
            direction.normalize_ip()
            self._state = consts.RUN

        self._side = pg.K_a if direction.x < 0 else pg.K_d

        self._call_all(state=self._state, side=self._side)
        if direction.x != 0 and direction.y != 0:
            self._move_object(direction * self._speed)


class BotMagicController(MagicController):
    def __init__(self, owner, player, cooldown=600):
        super().__init__(owner)
        self._player = player
        self._cooldown = cooldown
        self._last_attack = 0

    def attack(self):
        if not self._player.alive():
            return

        current_time = pg.time.get_ticks()
        if current_time - self._last_attack < self._cooldown:
            return

        bot_pos = pg.math.Vector2(self._owner.rect.center)
        player_pos = pg.math.Vector2(self._player.rect.center)
        distance = bot_pos.distance_to(player_pos)

        self._last_attack = current_time

        if distance < 150:
            self._state = random.choice([consts.ATTACK2, consts.ATTACK3])
        else:
            self._state = consts.ATTACK1

        self._attack_event(self._state, player_pos)

