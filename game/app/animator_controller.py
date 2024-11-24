import os
from typing import Any

import pygame as pg

from app import consts
from app.base.animator import Animator, Animation


class AnimationMapBuilder:
    def __init__(self):
        self.__animation_map = {}

    def build_from_files(self, folder, not_looped=()):
        files = os.listdir(folder)
        for anim in consts.ALL:
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

    def __set_animation(self, key, path, loop):
        self.__animation_map[key] = (path, loop)
        return self

    def attack1(self, path, loop=True):
        return self.__set_animation(consts.ATTACK1, path, loop)

    def attack2(self, path, loop=True):
        return self.__set_animation(consts.ATTACK2, path, loop)

    def attack3(self, path, loop=True):
        return self.__set_animation(consts.ATTACK3, path, loop)

    def climb(self, path, loop=True):
        return self.__set_animation(consts.CLIMB, path, loop)

    def death(self, path, loop=True):
        return self.__set_animation(consts.DEATH, path, loop)

    def hurt(self, path, loop=True):
        return self.__set_animation(consts.HURT, path, loop)

    def idle(self, path, loop=True):
        return self.__set_animation(consts.IDLE, path, loop)

    def jump(self, path, loop=True):
        return self.__set_animation(consts.JUMP, path, loop)

    def land(self, path, loop=True):
        return self.__set_animation(consts.LAND, path, loop)

    def run(self, path, loop=True):
        return self.__set_animation(consts.RUN, path, loop)

    def walk(self, path, loop=True):
        return self.__set_animation(consts.WALK, path, loop)

class AnimatorController(Animator):
    def __init__(self, side_mapper: dict[int, int], animations: dict[Any, Animation], default=None):
        super().__init__(animations, default)
        self.__side = pg.K_a

        self.__side_mapper = side_mapper

        self.replace_row(self.__side_mapper[self.__side])

    def move(self, side):
        self.__side = side
        self.replace_row(self.__side_mapper[self.__side])

    @property
    def side(self):
        return self.__side