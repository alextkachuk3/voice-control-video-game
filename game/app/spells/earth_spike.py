import pygame as pg

from app.spells.ice_spike import IceSpikeSpellSpawner

class EarthSpikeSpellSpawner(IceSpikeSpellSpawner):
    def __init__(self, *groups, scale=1.5, damage=6):
        super().__init__(*groups, speed=3, scale=scale, damage=damage)

        self._image = pg.image.load("Assets/Images/Spells/EarthSpike.png")
