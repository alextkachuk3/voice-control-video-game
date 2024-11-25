import pygame as pg

from app.spells.water_blast import WaterBlastSpellSpawner


class ToxicBlastSpellSpawner(WaterBlastSpellSpawner):
    def __init__(self, *groups, scale=1.5):
        super().__init__(*groups, scale=scale, timeout=60)

        self._image = pg.image.load("Assets/Images/Spells/ToxicBlast.png")
        self._image_attack = pg.image.load("Assets/Images/Spells/ToxicBlastAttack.png")

    def spawn(self, owner, pos):
        item = super().spawn(owner, pos)

        item.set_bounding_size((self._size[0]/3, self._size[1]/1.5))
        return item