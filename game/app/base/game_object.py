import pygame as pg

class GameObject(pg.sprite.Sprite):
    def __init__(self, name: str, pos: tuple[int, int], size:tuple[int, int],
                 *groups:pg.sprite.Group):
        super().__init__(*groups)
        self.name = name

        self.__image = pg.surface.Surface(size)
        self.__rect = self.__image.get_rect()
        self.__rect.center = pos

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect