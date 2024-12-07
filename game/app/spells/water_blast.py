import pygame as pg

from app import consts
from app.base.translator import tr
from app.spells.blast import BlastSpellSpawner


class WaterBlastSpellSpawner(BlastSpellSpawner):
    def __init__(self, *groups):
        super().__init__(*groups, scale=1, timeout=200, damage=10, cooldown=300,
                         activate_words=tr(consts.WATER_BLAST), icon=pg.image.load("Assets/Images/Icons/WaterBlast.png"))

        self._image = pg.image.load("Assets/Images/Spells/WaterBlast.png")
        self._image_attack = pg.image.load("Assets/Images/Spells/WaterBlastAttack.png")
