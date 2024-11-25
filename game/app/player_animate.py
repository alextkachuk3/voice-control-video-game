import os
from typing import Any

import pygame as pg

from app import consts
from app.base.animator import Animation, AnimationMapBuilder
from app.controllers.animate import AnimateController


def get_player_animations(size, delay, textures_folder:str, animation_map:dict[Any, tuple[str, bool]]):
    animations = {}

    for name in consts.ALL:
        if name not in animation_map:
            continue

        anim_name, loop = animation_map[name]
        filename = os.path.join(textures_folder, anim_name)
        image = pg.image.load(filename)
        animation = Animation(image, (0, 0), size, delay=delay, loop=loop)

        animations[name] = animation

    return animations


def get_animate_controller(size, folder, delay=8):
    builder = AnimationMapBuilder(animation_names=consts.ALL)
    anim_map = builder.build_from_files(folder, not_looped=(consts.ATTACK1, consts.ATTACK2, consts.ATTACK3))

    animators = get_player_animations(size, delay, folder, anim_map)

    anim_controller = AnimateController({
        pg.K_s: 0,
        pg.K_a: 1,
        pg.K_d: 2,
        pg.K_w: 3,
    }, animators, default=consts.IDLE)

    return anim_controller