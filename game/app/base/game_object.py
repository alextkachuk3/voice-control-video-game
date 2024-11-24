
import pygame as pg


class GameObject(pg.sprite.Sprite):
    def __init__(self, name: str, pos: tuple[int, int], size:tuple[int, int],
                 *groups:pg.sprite.Group, background=(1, 0, 0), transparent=(0, 0, 0)):
        super().__init__(*groups)
        self.name = name

        self.__image = pg.surface.Surface(size)
        self.__image.set_colorkey(transparent)
        self.__image.fill(background)

        self.__rect = self.__image.get_rect(center=pos)
        self.__bounding_size = None

        self._size= size
        self._angle = 0

    @property
    def bounding_rect(self):
        bounding_rect = self.image.get_bounding_rect() if self.__bounding_size is None \
            else pg.rect.Rect(0, 0, *self.__bounding_size)
        bounding_rect.center = self.__rect.center
        return bounding_rect.inflate(-bounding_rect.w/10, -bounding_rect.h/10)

    def set_bounding_size(self, bounding_size = None):
        self.__bounding_size = bounding_size

    def _prepare_image(self, image):
        return pg.transform.scale(pg.transform.rotate(image, self._angle), self._size)

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    def move_by(self, direction):
        self.__rect.center += direction

    def near_bounds(self, w, h):
        return self.rect.top <= 0 or self.rect.bottom >= h or self.rect.left <= 0 or self.rect.right >= w

    def rotate(self, angle):
        center = self.__rect.center
        self._angle=angle

        self.__image = pg.transform.rotate(self.__image, angle)
        self.__rect = self.__image.get_rect(center=center)