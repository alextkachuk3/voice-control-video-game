from math import ceil
from random import randint

import pygame as pg


def grid_count(grid_size, cell_size):
    rows = int(ceil(grid_size[1] / cell_size[1]))
    cols = int(ceil(grid_size[0] / cell_size[0]))

    return rows, cols


class TailMapBuilder:
    def __init__(self, image: pg.surface.Surface,
                 surface_size: tuple[int, int], tail_size: tuple[int, int], transparent="black"):

        self.__image = image
        self.__tail_rows, self.__tail_cols = grid_count(self.__image.get_size(), tail_size)
        self.__x, self.__y = (0, 0)
        self.__surface_size = surface_size
        self.__tail_size = tail_size

        self.__transparent = transparent
        self.__map = pg.surface.Surface(surface_size)
        self.__map.fill(transparent)
        self.__map.set_colorkey(transparent)
        self.__row = 0
        self.__col = 0
        self.__cols, self.__rows = grid_count(surface_size, tail_size)

    def add_tail(self, tail_place, map_place=None, map_size=None):
        if tail_place[0] >= self.__tail_cols or tail_place[1] >= self.__tail_rows:
            raise ValueError("Tail place out of bounds")

        if map_size is None:
            map_size = self.__tail_size

        w, h = map_size

        if map_place is None:
            map_place = self.__row, self.__col
            self.__col += 1
            if self.__col >= self.__cols:
                self.__col = 0
                self.__row += 1

        row, col = map_place
        place_x = col * w
        place_y = row * h
        tail_row, tail_col = tail_place

        tail = self.__image.subsurface((self.__x + tail_col * w, self.__y + tail_row * h, w, h))
        self.__map.blit(tail, (place_x, place_y, w, h))

        return self

    def fill(self, tail_place):
        if tail_place[1] >= self.__tail_cols or tail_place[0] >= self.__tail_rows:
            raise ValueError("Tail place out of bounds")

        w, h = self.__tail_size
        tail_row, tail_col = tail_place
        tail = self.__image.subsurface((tail_col * w, tail_row * h, w, h))

        for i in range(self.__rows):
            for j in range(self.__cols):
                self.__map.blit(tail, (i * w, j * h, w, h))

        return self

    def fill_random(self):
        w, h = self.__tail_size

        for i in range(self.__rows):
            for j in range(self.__cols):
                row = randint(0, self.__tail_rows - 1)
                col = randint(0, self.__tail_cols - 1)

                tail = self.__image.subsurface((col * w, row * h, w, h))
                self.__map.blit(tail, (i * w, j * h, w, h))

        return self

    def tail_map(self):
        return self.__map

    def clear(self):
        self.__map.fill(self.__transparent)
