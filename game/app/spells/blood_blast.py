import pygame as pg

from app.spells.water_blast import WaterBlastSpellSpawner


class BloodBlastSpellSpawner(WaterBlastSpellSpawner):
    def __init__(self, *groups, scale=0.8, timeout=100, damage=12, cooldown=200):
        super().__init__(*groups, scale=scale, timeout=timeout, damage=damage, cooldown=cooldown)

        self._image = pg.image.load("Assets/Images/Spells/BloodBlast.png")
        self._image_attack = pg.image.load("Assets/Images/Spells/BloodBlastAttack.png")

    def spawn(self, owner, pos):
        item = super().spawn(owner, pos)

        item.set_bounding_size((self._size[0] / 3, self._size[1] / 1.5))
        return item
