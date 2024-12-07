import pygame as pg

from app import consts
from app.base.animator import Animation, Animator
from app.spells.spell import MoveSpellSpawner


class SpikeSpellSpawner(MoveSpellSpawner):
    def __init__(self, *groups, scale=1, speed=1, damage=1, cooldown=1, activate_words=()):
        self.__w, self.__h = 48, 32
        super().__init__(consts.ATTACK, (self.__w * scale, self.__h * scale), *groups,
                         speed=speed, damage=damage, cooldown=cooldown, activate_words=activate_words)

        self._image = pg.surface.Surface((self.__w, self.__h))

    def _get_animator(self):
        animation_spawn = Animation(self._image, (0, self.__h), (self.__w, self.__h), max_frames=3, delay=7, loop=False)
        animation_idle = Animation(self._image, (0, 0), (self.__w, self.__h), delay=3)
        animation_attack = Animation(self._image, (0, 2 * self.__h), (self.__w, self.__h), max_frames=7, delay=5,
                                     loop=False)

        animator = Animator({
            consts.SPAWN: animation_spawn,
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        animator.replace_animation(consts.SPAWN)

        return animator
