import pygame as pg

from app import consts
from app.base.translator import tr
from app.spells.blast import BlastSpellSpawner


class BloodBlastSpellSpawner(BlastSpellSpawner):
    def __init__(self, *groups):
        super().__init__(*groups, scale=0.8, timeout=100, damage=12, cooldown=200,
                         activate_words=tr(consts.BLOOD_BLAST),
                         icon=pg.image.load("Assets/Images/Icons/BloodBlast.png"))

        self._image = pg.image.load("Assets/Images/Spells/BloodBlast.png")
        self._image_attack = pg.image.load("Assets/Images/Spells/BloodBlastAttack.png")

    def spawn(self, owner, pos):
        item = super().spawn(owner, pos)

        item.set_bounding_size((self._size[0] / 3, self._size[1] / 1.5))
        return item
