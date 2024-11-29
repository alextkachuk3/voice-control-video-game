import pygame as pg

from app import consts
from app.spells.ice_spike import IceSpikeSpellSpawner


class EarthSpikeSpellSpawner(IceSpikeSpellSpawner):
    def __init__(self, *groups, scale=1.5, damage=6, cooldown=40, activate_words=consts.EARTH_SPIKE):
        super().__init__(*groups, speed=3, scale=scale, damage=damage, cooldown=cooldown,
                         activate_words=activate_words)

        self._image = pg.image.load("Assets/Images/Spells/EarthSpike.png")
