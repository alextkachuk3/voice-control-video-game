from typing import Any

import pygame as pg


class Animation:
    def __init__(self, image:pg.surface.Surface, start_pos:tuple[int, int], rect_size:tuple[int, int],
                 transparent_color="black", max_frames=0, delay=0, loop=True):
        self.__full_image = image.convert_alpha()
        self.__full_image.set_colorkey(transparent_color)

        self.__loop = loop
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
        self.__ended = False

    @property
    def ended(self):
        return self.__ended

    def next_frame(self):
        if self.__ended:
            return

        self.__current_delay += 1
        if self.__current_delay < self.__delay:
            return

        self.__current_delay = 0
        self.__index += 1
        if self.__index >= self.__frames:
            self.__index = 0
            self.__ended = not self.__loop

    def reset(self):
        self.__index = 0
        self.__ended = False

    def get_image(self, row=0):
        return self.__full_image.subsurface((self.__x + self.__index*self.__w,
                                             self.__y + row*self.__h, self.__w, self.__h))


class Animator:
    def __init__(self, animations: dict[Any, Animation], default=None):
        self.__animations = animations
        if len(self.__animations) == 0:
            raise ValueError("Animations dictionary is empty!")

        self.__default = default if default else next(iter(animations.keys()))
        self.__current_anim = self.__default

    def replace_animation(self, anim_name=None):
        if anim_name is None or anim_name not in self.__animations:
            anim_name = self.__default

        if anim_name != self.__current_anim:
            self.__current_anim = anim_name
            self.__animations[anim_name].reset()

    def tick(self):
        anim = self.__animations[self.__current_anim]
        anim.next_frame()
        if anim.ended:
            self.replace_animation()

    def get_image(self, row=0):
        return self.__animations[self.__current_anim].get_image(row)

    @property
    def animation_name(self):
        return self.__current_anim
