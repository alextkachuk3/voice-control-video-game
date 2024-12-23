import pygame as pg

from app import consts
from app.base.translator import tr
from app.spells.blast import BlastSpellSpawner


class ToxicBlastSpellSpawner(BlastSpellSpawner):
    def __init__(self, *groups):
        super().__init__(*groups, scale=1.5, timeout=60, damage=10, cooldown=120,
                         activate_words=tr(consts.TOXIC_BLAST), icon=pg.image.load("Assets/Images/Icons/ToxicBlast.png"))

        self._image = pg.image.load("Assets/Images/Spells/ToxicBlast.png")
        self._image_attack = pg.image.load("Assets/Images/Spells/ToxicBlastAttack.png")

    def spawn(self, owner, pos):
        item = super().spawn(owner, pos)

        item.set_bounding_size((self._size[0] / 3, self._size[1] / 1.5))
        return item
