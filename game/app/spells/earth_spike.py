import pygame as pg

from app.spells.ice_spike import IceSpikeSpellSpawner

class EarthSpikeSpellSpawner(IceSpikeSpellSpawner):
    def __init__(self, *groups, scale=1.5):
        super().__init__(*groups, speed=3, scale=scale)

        self._image = pg.image.load("Assets/Images/Spells/EarthSpike.png")
