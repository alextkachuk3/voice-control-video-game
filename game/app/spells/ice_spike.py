import pygame as pg

from app import consts
from app.base.translator import tr
from app.spells.spike import SpikeSpellSpawner


class IceSpikeSpellSpawner(SpikeSpellSpawner):
    def __init__(self, *groups):
        super().__init__(*groups, speed=5, scale=1, damage=8, cooldown=60,
                         activate_words=tr(consts.ICE_SPIKE))

        self._image = pg.image.load("Assets/Images/Spells/IceSpike.png")

