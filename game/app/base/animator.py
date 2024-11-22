from typing import Any

import pygame as pg


class Animation:
    def __init__(self, image:pg.surface.Surface, start_pos:tuple[int, int], rect_size:tuple[int, int],
                 transparent_color="black", max_frames=0, delay=0):
        self.__full_image = image.convert_alpha()
        self.__full_image.set_colorkey(transparent_color)

        self.__delay = delay
        self.__current_delay = 0

        self.__x, self.__y = start_pos
        self.__w, self.__h = rect_size
        self.__frames = self.__full_image.get_width()//self.__w
        if max_frames != 0:
            self.__frames = max(max_frames, self.__frames)

        if self.__frames == 0:
            raise ValueError("Image size is too small or rect size is too big!")

        self.__index = 0

        self.__transparent_color = transparent_color

    def next_frame(self):
        self.__current_delay += 1
        if self.__current_delay < self.__delay:
            return

        self.__current_delay = 0
        self.__index += 1
        if self.__index >= self.__frames:
            self.__index = 0

    def reset(self):
        self.__index = 0

    def get_image(self, row=0):
        return self.__full_image.subsurface((self.__x + self.__index*self.__w,
                                             self.__y + row*self.__h, self.__w, self.__h))


class Animator:
    def __init__(self, animations: dict[Any, Animation]):
        self.__animations = animations
        if len(self.__animations) == 0:
            raise ValueError("Animations dictionary is empty!")

        self.__current_anim = next(iter(animations.keys()))

    def replace_animation(self, anim_name):
        if anim_name not in self.__animations:
            anim_name = next(iter(self.__animations.keys()))

        if anim_name != self.__current_anim:
            self.__current_anim = anim_name
            self.__animations[anim_name].reset()

    def tick(self):
        self.__animations[self.__current_anim].next_frame()

    def get_image(self, row=0):
        return self.__animations[self.__current_anim].get_image(row)