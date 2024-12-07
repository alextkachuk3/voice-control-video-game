import pygame as pg

from app.spells.spell import SpellSpawner


class SpellIcon(pg.sprite.Sprite):
    def __init__(self, size, topleft, spell_spawner:SpellSpawner, *groups):
        super().__init__(*groups)

        if spell_spawner.icon:
            self.image = pg.transform.scale(spell_spawner.icon, size)
        else:
            self.image = pg.surface.Surface(size)
            self.image.fill("white")

        self.shade = pg.surface.Surface(size)
        self.shade.set_colorkey((0, 0, 1))

        self.rect = self.image.get_rect(topleft=topleft)

        self.__spell_spawner = spell_spawner
        self.__w, self.__h = size

    def update(self):
        self.shade.fill((0, 0, 1))
        h = int(self.__spell_spawner.ready_by()*self.__h)
        pg.draw.rect(self.shade, (0, 0, 0, 100), (0, h, self.__w,  self.__h - h))



class SpellPanel(pg.sprite.Sprite):
    def __init__(self, size, midtop, background, *groups):
        super().__init__(*groups)

        self.image = pg.Surface(size)
        self.image.fill(background)
        self.__background = background

        self.rect = self.image.get_rect(midtop=midtop)
        self.__spells = []

    def add_spell(self, spell_icon):
        self.__spells.append(spell_icon)

    def update(self):
        self.image.fill(self.__background)

        for spell in self.__spells:
            spell.update()
            self.image.blit(spell.image, spell.rect)
            self.image.blit(spell.shade, spell.rect)

