from app import consts
from app.base.animator import Animation, Animator

import pygame as pg

from app.consts import CAST_RADIUS
from app.spells.spell import TargetSpellSpawner


class MineSpellSpawner(TargetSpellSpawner):
    def __init__(self, *groups, scale=1, damage=15):
        self.__w, self.__h = 64, 64
        super().__init__(consts.ATTACK, (self.__w*scale, self.__h*scale), *groups,
                         radius=CAST_RADIUS, damage=damage)

        self.__image = pg.image.load("Assets/Images/Spells/Mine.png")

    def _get_animator(self):
        animation_idle = Animation(self.__image , (0, 0), (self.__w,self.__h), max_frames=2, delay=10)
        animation_attack = Animation(self.__image , (2*self.__w, 0), (self.__w, self.__h), delay=5,
                                     loop=False, auto_row=True)

        animator = Animator({
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        return animator

    def spawn(self, owner, pos):
        item = super().spawn(owner, pos)

        item.set_bounding_size((self._size[0]/4, self._size[1]/4))
        return item