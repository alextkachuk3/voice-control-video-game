import pygame as pg

from app import consts
from app.background import get_random_background
from app.base.game_object import GameObject
from app.base.scene import Scene
from app.player import KeyboardPlayer
from app.player_animate import get_animate_controller
from app.spells.firebolt import FireboltSpellSpawner
from app.spells.ice_spike import IceSpikeSpellSpawner
from app.spells.water_blast import WaterBlastSpellSpawner


class TrainingScene(Scene):
    __title__ = "Training"
    DEBUG=False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()

        self.player_group = pg.sprite.Group()
        self.spell_group = pg.sprite.Group()

        pg.mouse.set_visible(False)
        self.cursor = GameObject("cursor", (0, 0), (20, 20), self._draw_group,
                                 image=pg.image.load("Assets/Images/target-mask.png"), background="white")

        animator_controller = get_animate_controller((48, 48), "Assets/Images/Characters/Necromancer")
        self.player = KeyboardPlayer((w // 2, h // 2), (100, 100), self.player_group, self._draw_group,
                                     speed=2, anim_controller=animator_controller)

        self.player.set_bounding_size((30, 60))

        self.player.add_spell(consts.ATTACK1, FireboltSpellSpawner(1,  self.spell_group, self._draw_group))
        self.player.add_spell(consts.ATTACK2, IceSpikeSpellSpawner(1,  self.spell_group, self._draw_group))
        self.player.add_spell(consts.ATTACK3, WaterBlastSpellSpawner(1, self.spell_group, self._draw_group))

        self.bg = get_random_background("Assets/Images/TailMaps/GrassTileset.png", (w, h), (32, 32))


    def draw(self):
        super().draw()
        if self.DEBUG:
            for obj in self._draw_group:
                pg.draw.rect(self, "black",obj.bounding_rect, width=1)
            pg.draw.circle(self, "black", self.player.rect.center, radius=150, width=1)
    def draw_background(self):
        self.blit(self.bg, (0, 0))

    def update(self):
        self.cursor.rect.center = pg.mouse.get_pos()

        self.player_group.update()
        self.spell_group.update(self.player_group)

        self._clock.tick(60)
