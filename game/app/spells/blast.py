import pygame as pg

from app import consts
from app.base.animator import Animation, Animator
from app.consts import CAST_RADIUS
from app.spells.spell import TargetSpellSpawner


class BlastSpellSpawner(TargetSpellSpawner):
    def __init__(self, *groups, scale=1, timeout=1, damage=1, cooldown=1, activate_words=()):
        self.__w, self.__h = 128, 128
        super().__init__(consts.ATTACK, (self.__w * scale, self.__h * scale), *groups,
                         radius=CAST_RADIUS, timeout=timeout, damage=damage, cooldown=cooldown,
                         activate_words=activate_words)

        self._image = pg.surface.Surface((self.__w, self.__h))
        self._image_attack = pg.surface.Surface((self.__w, self.__h))

    def _get_animator(self):
        animation_spawn = Animation(self._image, (0, 0), (self.__w, self.__h), max_frames=4, delay=12, loop=False)
        animation_idle = Animation(self._image, (0, self.__h), (self.__w, self.__h), delay=4, auto_row=True)
        animation_attack = Animation(self._image_attack, (0, 0), (self.__w, self.__h), delay=5, loop=False,
                                     auto_row=True)

        animator = Animator({
            consts.SPAWN: animation_spawn,
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        animator.replace_animation(consts.SPAWN)

        return animator
