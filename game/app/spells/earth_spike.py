import pygame as pg

from app import consts
from app.base.translator import tr
from app.spells.spike import SpikeSpellSpawner


class EarthSpikeSpellSpawner(SpikeSpellSpawner):
    def __init__(self, *groups):
        super().__init__(*groups, speed=3, scale=1.5, damage=6, cooldown=40,
                         activate_words=tr(consts.EARTH_SPIKE),
                         icon=pg.image.load("Assets/Images/Icons/EarthSpike.png"))

        self._image = pg.image.load("Assets/Images/Spells/EarthSpike.png")
