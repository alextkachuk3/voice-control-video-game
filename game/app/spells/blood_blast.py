from app import consts
from app.base.animator import Animation, Animator

import pygame as pg

from app.consts import CAST_RADIUS
from app.spells.spell import TargetSpellSpawner
from app.spells.water_blast import WaterBlastSpellSpawner


class BloodBlastSpellSpawner(WaterBlastSpellSpawner):
    def __init__(self, *groups, scale=0.8):
        super().__init__(*groups, scale=scale)

        self._image = pg.image.load("Assets/Images/Spells/BloodBlast.png")
        self._image_attack = pg.image.load("Assets/Images/Spells/BloodBlastAttack.png")

    def spawn(self, owner, pos):
        item = super().spawn(owner, pos)

        item.set_bounding_size((self._size[0]/3, self._size[1]/1.5))
        return item