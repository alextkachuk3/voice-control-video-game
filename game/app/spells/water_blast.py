from app import consts
from app.base.animator import Animation, Animator

import pygame as pg

from app.spell import TargetSpellSpawner


class WaterBlastSpellSpawner(TargetSpellSpawner):
    def __init__(self, scale, *groups):
        self.__w, self.__h = 128, 128
        super().__init__(consts.ATTACK, (self.__w*scale, self.__h*scale), *groups, radius=150)

        self.__image = pg.image.load("Assets/Images/Spells/WaterBlast.png")
        self.__image_attack = pg.image.load("Assets/Images/Spells/WaterBlastAttack.png")

    def _get_animator(self):
        animation_spawn = Animation(self.__image , (0, 0), (self.__w,self.__h), max_frames=4, delay=12, loop=False)
        animation_idle = Animation(self.__image , (0, self.__h), (self.__w,self.__h), delay=4, auto_row=True)
        animation_attack = Animation(self.__image_attack , (0, 0), (self.__w, self.__h), delay=5, loop=False, auto_row=True)

        animator = Animator({
            consts.SPAWN:animation_spawn,
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        animator.replace_animation(consts.SPAWN)

        return animator