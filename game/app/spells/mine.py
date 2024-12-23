import pygame as pg

from app import consts
from app.base.animator import Animation, Animator
from app.base.translator import tr
from app.consts import CAST_RADIUS
from app.spells.spell import TargetSpellSpawner


class MineSpellSpawner(TargetSpellSpawner):
    def __init__(self, *groups):
        self.__w, self.__h = 64, 64
        scale = 1

        super().__init__(consts.ATTACK, (self.__w * scale, self.__h * scale), *groups,
                         radius=CAST_RADIUS, damage=15, cooldown=200, activate_words=tr(consts.MINE),
                         icon=pg.image.load("Assets/Images/Icons/Mine.png"))

        self.__image = pg.image.load("Assets/Images/Spells/Mine.png")

    def _get_animator(self):
        animation_spawn = Animation(self.__image, (0, 0), (self.__w, self.__h), max_frames=2,
                                    delay=50, loop=False)

        animation_idle = Animation(self.__image, (0, 0), (self.__w, self.__h), max_frames=2, delay=10)
        animation_attack = Animation(self.__image, (2 * self.__w, 0), (self.__w, self.__h), delay=5,
                                     loop=False, auto_row=True)

        animator = Animator({
            consts.SPAWN: animation_spawn,
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        animator.replace_animation(consts.SPAWN)

        return animator

    def spawn(self, owner, pos):
        item = super().spawn(owner, pos)

        item.set_bounding_size((self._size[0] / 4, self._size[1] / 4))
        return item
