from app import consts
from app.base.animator import Animation, Animator

import pygame as pg

from app.spells.spell import MoveSpellSpawner

class IceSpikeSpellSpawner(MoveSpellSpawner):
    def __init__(self, *groups, scale=1):
        self.__w, self.__h = 48, 32
        super().__init__(consts.ATTACK, (self.__w*scale, self.__h*scale),  *groups, speed=5)

        self.__image = pg.image.load("Assets/Images/Spells/IceSpike.png")

    def _get_animator(self):
        animation_spawn = Animation(self.__image , (0, self.__h), (self.__w,self.__h), max_frames=3, delay=7, loop=False)
        animation_idle = Animation(self.__image , (0, 0), (self.__w,self.__h), delay=3)
        animation_attack = Animation(self.__image , (0, 2*self.__h), (self.__w, self.__h), max_frames=7, delay=5, loop=False)

        animator = Animator({
            consts.SPAWN:animation_spawn,
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        animator.replace_animation(consts.SPAWN)

        return animator
