
import pygame as pg


class GameObject(pg.sprite.Sprite):
    def __init__(self, name: str, pos: tuple[int, int], size:tuple[int, int],
                 *groups:pg.sprite.Group, background="black", transparent_color="black", image=None):
        super().__init__(*groups)
        self.name = name
        self._size= size
        self._angle = 0
        self.__transparent_color = transparent_color

        self.__image = pg.surface.Surface(size)
        self.__image.set_colorkey(transparent_color)
        self.__image.fill(background)
        if image:
            self.__image.blit(self._prepare_image(image, False), (0, 0))


        self.__rect = self.__image.get_rect(center=pos)
        self.__bounding_size = None

    @property
    def bounding_rect(self):
        bounding_rect = self.image.get_bounding_rect() if self.__bounding_size is None \
            else pg.rect.Rect(0, 0, *self.__bounding_size)
        bounding_rect.center = self.__rect.center
        return bounding_rect

    def set_bounding_size(self, bounding_size = None):
        self.__bounding_size = bounding_size

    def _prepare_image(self, image, transparent=True):
        image = pg.transform.scale(pg.transform.rotate(image, self._angle), self._size)
        if transparent:
            image.set_colorkey(self.__transparent_color)

        return image

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    def move_by(self, direction):
        self.__rect.center += direction

    def near_bounds(self, w, h):
        return self.bounding_rect.top <= 0 or self.bounding_rect.bottom >= h \
            or self.bounding_rect.left <= 0 or self.bounding_rect.right >= w

    def rotate(self, angle):
        center = self.__rect.center
        self._angle=angle

        self.__image = pg.transform.rotate(self.__image, angle)
        self.__rect = self.__image.get_rect(center=center)