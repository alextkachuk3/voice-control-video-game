import os
from typing import Any

import pygame as pg

from app.base.animator import Animator, Animation


class AnimationMapBuilder:
    ATTACK1 = "attack01"
    ATTACK2 = "attack02"
    ATTACK3 = "attack03"
    CLIMB = "climb"
    DEATH = "death"
    HURT = "hit"
    IDLE = "idle"
    JUMP = "jump"
    LAND = "land"
    RUN = "run"
    WALK = "walk"

    ALL = [ATTACK1, ATTACK2, ATTACK3, CLIMB, DEATH, HURT, IDLE,JUMP,LAND,RUN,WALK]

    def __init__(self):
        self.__animation_map = {}

    def build_from_files(self, folder, not_looped=()):
        files = os.listdir(folder)
        for anim in self.ALL:
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
        return self.__set_animation(self.ATTACK1, path, loop)

    def attack2(self, path, loop=True):
        return self.__set_animation(self.ATTACK2, path, loop)

    def attack3(self, path, loop=True):
        return self.__set_animation(self.ATTACK3, path, loop)

    def climb(self, path, loop=True):
        return self.__set_animation(self.CLIMB, path, loop)

    def death(self, path, loop=True):
        return self.__set_animation(self.DEATH, path, loop)

    def hurt(self, path, loop=True):
        return self.__set_animation(self.HURT, path, loop)

    def idle(self, path, loop=True):
        return self.__set_animation(self.IDLE, path, loop)

    def jump(self, path, loop=True):
        return self.__set_animation(self.JUMP, path, loop)

    def land(self, path, loop=True):
        return self.__set_animation(self.LAND, path, loop)

    def run(self, path, loop=True):
        return self.__set_animation(self.RUN, path, loop)

    def walk(self, path, loop=True):
        return self.__set_animation(self.WALK, path, loop)

class AnimatorController:
    def __init__(self, animator:Animator, side_mapper:dict[int, int]):
        self.__side = pg.K_a

        self.__animator = animator
        self.__animator.replace_animation(AnimationMapBuilder.IDLE)

        self.__side_mapper = side_mapper

    def move(self, side):
        self.__side = side

    def replace_animation(self, anim_name):
        self.__animator.replace_animation(anim_name)

    def tick(self):
        self.__animator.tick()

    @property
    def image(self):
        return self.__animator.get_image(row=self.__side_mapper[self.__side])

    @property
    def animation_name(self):
        return self.__animator.animation_name

    @property
    def side(self):
        return self.__side

def get_player_animator(size, delay, textures_folder:str, animation_map:dict[Any, tuple[str, bool]]):
    animations = {}

    for name in AnimationMapBuilder.ALL:
        if name not in animation_map:
            continue

        anim_name, loop = animation_map[name]
        filename = os.path.join(textures_folder, anim_name)
        image = pg.image.load(filename)
        animation = Animation(image, (0, 0), size, delay=delay, loop=loop)

        animations[name] = animation

    return Animator(animations, AnimationMapBuilder.IDLE)


def get_animator_controller(size, folder, delay=7):
    builder = AnimationMapBuilder()
    anim_map = builder.build_from_files(folder, not_looped=(AnimationMapBuilder.ATTACK1, AnimationMapBuilder.ATTACK2, AnimationMapBuilder.ATTACK3))

    animator = get_player_animator(size, delay, folder, anim_map)

    anim_controller = AnimatorController(animator, {
        pg.K_s: 0,
        pg.K_a: 1,
        pg.K_d: 2,
        pg.K_w: 3,
    })

    return anim_controller