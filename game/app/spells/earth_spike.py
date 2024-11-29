import pygame as pg

from app.spells.ice_spike import IceSpikeSpellSpawner

class EarthSpikeSpellSpawner(IceSpikeSpellSpawner):
    def __init__(self, *groups, scale=1.5, damage=6, cooldown=40):
        super().__init__(*groups, speed=3, scale=scale, damage=damage, cooldown=cooldown)

        self._image = pg.image.load("Assets/Images/Spells/EarthSpike.png")
