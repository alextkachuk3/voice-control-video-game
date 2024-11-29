import os
from typing import Any

import pygame as pg

from app.base.game_object import GameObject


class Animation:
    def __init__(self, image: pg.surface.Surface, start_pos: tuple[int, int], rect_size: tuple[int, int],
                 transparent_color="black", max_frames=0, delay=0, loop=True, auto_row=False, max_rows=0):
        self.__full_image = image.convert_alpha()
        self.__full_image.set_colorkey(transparent_color)

        self.__loop = loop
        self.__delay = delay
        self.__current_delay = 0

        self.__x, self.__y = start_pos
        self.__w, self.__h = rect_size
        self.__frames = (self.__full_image.get_width() - self.__x) // self.__w
        if max_frames != 0:
            self.__frames = min(max_frames, self.__frames)

        if self.__frames == 0:
            raise ValueError("Image size is too small or rect size is too big!")

        self.__index = 0

        self.__transparent_color = transparent_color
        self.__ended = False

        self.__row = 0
        self.__rows = (self.__full_image.get_height() - self.__y) // self.__h
        self.__auto_row = auto_row

        if max_rows != 0:
            self.__rows = min(max_rows, self.__rows)

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
        if self.__index < self.__frames:
            return
        self.__index = 0 if self.__loop else (self.__frames - 1)
        self.__ended = not self.__loop

        if not self.__auto_row:
            return

        self.__row += 1
        self.__index = 0
        self.__ended = False
        if self.__row >= self.__rows:
            self.__row = 0 if self.__loop else (self.__rows - 1)
            self.__index = 0 if self.__loop else (self.__frames - 1)
            self.__ended = not self.__loop

    def reset(self):
        self.__index = 0
        self.__ended = False

    def get_image(self, row=0):
        if self.__auto_row:
            row = self.__row

        image = self.__full_image.subsurface((self.__x + self.__index * self.__w,
                                              self.__y + row * self.__h, self.__w, self.__h))
        image.set_colorkey(self.__transparent_color)

        return image


class Animator:
    def __init__(self, animations: dict[Any, Animation], default=None):
        self.__animations = animations
        if len(self.__animations) == 0:
            raise ValueError("Animations dictionary is empty!")

        self.__default = default if default else next(iter(animations.keys()))
        self.__current_anim = self.__default

        self.__end_callbacks = {}
        self.__row = 0

    def replace_row(self, row=0):
        self.__row = row

    def subscribe_to_end(self, callback, keys=()):
        callbacks = self.__end_callbacks.get(keys, [])
        callbacks.append(callback)
        self.__end_callbacks[keys] = callbacks

    def unsubscribe_from_end(self, callback, keys=()):
        callbacks = self.__end_callbacks.get(keys, [])
        callbacks.remove(callback)
        self.__end_callbacks[keys] = callbacks

    def replace_animation(self, anim_name=None, save_state=False):
        if anim_name is None or anim_name not in self.__animations:
            anim_name = self.__default

        if anim_name != self.__current_anim:
            self.__current_anim = anim_name
            if not save_state:
                self.__animations[anim_name].reset()

    def tick(self):
        anim = self.__animations[self.__current_anim]
        anim.next_frame()
        if not anim.ended:
            return

        for callback_key in self.__end_callbacks:
            if self.__current_anim not in callback_key and len(callback_key) > 0:
                continue

            for callback in self.__end_callbacks[callback_key]:
                callback()

        self.replace_animation()

    @property
    def image(self):
        return self.__animations[self.__current_anim].get_image(self.__row)

    @property
    def animation_name(self):
        return self.__current_anim

    def active(self, animation_name):
        return self.__current_anim == animation_name


class AnimationMapBuilder:
    def __init__(self, animation_names: list[str]):
        self.__animation_map = {}
        self.__animation_names = animation_names

    def build_from_files(self, folder, not_looped=()):
        files = os.listdir(folder)
        for anim in self.__animation_names:
            for file in files:
                if anim in file.lower():
                    self.__animation_map[anim] = (file, anim not in not_looped)
                    files.remove(file)
                    break

        return self.__animation_map

    def animation_map(self):
        return self.__animation_map

    def clear(self):
        self.__animation_map = {}
        return self

    def add_animation(self, key, path, loop):
        self.__animation_map[key] = (path, loop)
        return self


class AnimatedObject(GameObject):
    def __init__(self, name: str, pos: tuple[int, int], size: tuple[int, int],
                 *groups: pg.sprite.Group, animator=None, transparent_color="black"):
        super().__init__(name, pos, size, *groups, transparent_color=transparent_color)

        self._animator = animator

    def set_animator(self, animator):
        self._animator = animator

    def update(self, *args, **kwargs):
        if self._animator:
            self._animator.tick()

    @property
    def image(self):
        return super().image if self._animator is None else self._animator.image
