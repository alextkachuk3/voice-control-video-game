import pygame as pg

from app import env
from app.background import get_random_background
from app.base.scene import Scene
from app.player import KeyboardPlayer
from app.player_animator import get_animator_controller
from app.spells.firebolt import FireboltSpellSpawner
from app.spells.ice_spike import IceSpikeSpellSpawner
from app.spells.water_blast import WaterBlastSpellSpawner


class GameScene(Scene):
    __title__ = "GameScene"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()

        self.player_group = pg.sprite.Group()
        self.spell_group = pg.sprite.Group()

        animator_controller = get_animator_controller((48, 48), "Assets/Images/Characters/Necromancer")
        self.player = KeyboardPlayer((w // 2, h // 2), (100, 100), self.player_group, 2, animator_controller)
        self.player.add_spell(env.ATTACK1, FireboltSpellSpawner(1,  self.spell_group, speed=3))
        self.player.add_spell(env.ATTACK2, IceSpikeSpellSpawner(1,  self.spell_group, speed=5))
        self.player.add_spell(env.ATTACK3, WaterBlastSpellSpawner(1, self.spell_group))
        self.bg = get_random_background("Assets/Images/TailMaps/GrassTileset.png", (w, h), (32, 32))


    def draw(self):
        super().draw()
        self.player_group.draw(self)
        self.spell_group.draw(self)
        for spell in self.spell_group:
            pg.draw.rect(self, "black",spell.bounding_rect, width=1)
        pg.draw.rect(self, "black", self.player.bounding_rect, width=1)
    def draw_background(self):
       self.blit(self.bg, (0, 0))

    def update(self):
        self.player_group.update()
        self.spell_group.update(self.player_group)

        self._clock.tick(60)
