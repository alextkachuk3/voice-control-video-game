import pygame as pg

from app import consts
from app.base.animator import Animation, Animator
from app.spells.spell import MoveSpellSpawner


class FireboltSpellSpawner(MoveSpellSpawner):
    def __init__(self, *groups, scale=1, damage=7, cooldown=40, activate_words=consts.FIREBOLT):
        self.__w, self.__h = 48, 48
        super().__init__(consts.ATTACK, (self.__w * scale, self.__h * scale), *groups, speed=3,
                         damage=damage, cooldown=cooldown, activate_words=activate_words)

        self.__image = pg.image.load("Assets/Images/Spells/Firebolt.png")

    def _get_animator(self):
        animation_idle = Animation(self.__image, (0, 0), (self.__w, self.__h), max_frames=4, delay=5)
        animation_attack = Animation(self.__image, (self.__w * 5, 0), (self.__w, self.__h), delay=5, loop=False)

        animator = Animator({
            consts.IDLE: animation_idle,
            self._attack_type: animation_attack
        }, default=consts.IDLE)

        return animator

    def spawn(self, owner, pos, direction, speed=None):
        spell = super().spawn(owner, pos, direction, speed)
        spell.set_bounding_size((self.__w - 10, self.__h // 3))

        return spell
