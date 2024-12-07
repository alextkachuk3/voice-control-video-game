import pygame as pg

from app import consts
from app.base.animator import Animation, Animator
from app.base.translator import tr
from app.consts import CAST_RADIUS
from app.spells.spell import TargetSpellSpawner


class ExplosionSpellSpawner(TargetSpellSpawner):
    def __init__(self, *groups):
        self.__w, self.__h = 48, 48
        scale = 2

        super().__init__(consts.ATTACK, (self.__w * scale, self.__h * scale), *groups,
                         radius=CAST_RADIUS, timeout=60, damage=14, cooldown=120,
                         activate_words=tr(consts.EXPLOSION), icon=pg.image.load("Assets/Images/Icons/Explosion.png"))

        self.__image = pg.image.load("Assets/Images/Spells/Explosion.png")

    def _get_animator(self):
        animation_spawn = Animation(self.__image, (0, 0), (self.__w, self.__h), delay=10, max_frames=3, loop=False)
        animation_idle = Animation(self.__image, (0, 0), (self.__w, self.__h), delay=4, max_frames=3)
        animation_attack = Animation(self.__image, (3 * self.__w, 0), (self.__w, self.__h), delay=5, loop=False)

        animator = Animator({
            consts.SPAWN: animation_spawn,
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        animator.replace_animation(consts.SPAWN)

        return animator
