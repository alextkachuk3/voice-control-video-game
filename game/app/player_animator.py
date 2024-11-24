import os
from email.policy import default
from typing import Any

import pygame as pg

from app import env
from app.animator_controller import AnimationMapBuilder, AnimatorController
from app.base.animator import Animation


def get_player_animations(size, delay, textures_folder:str, animation_map:dict[Any, tuple[str, bool]]):
    animations = {}

    for name in env.ALL:
        if name not in animation_map:
            continue

        anim_name, loop = animation_map[name]
        filename = os.path.join(textures_folder, anim_name)
        image = pg.image.load(filename)
        animation = Animation(image, (0, 0), size, delay=delay, loop=loop)

        animations[name] = animation

    return animations


def get_animator_controller(size, folder, delay=7):
    builder = AnimationMapBuilder()
    anim_map = builder.build_from_files(folder, not_looped=(env.ATTACK1, env.ATTACK2, env.ATTACK3))

    animators = get_player_animations(size, delay, folder, anim_map)

    anim_controller = AnimatorController({
        pg.K_s: 0,
        pg.K_a: 1,
        pg.K_d: 2,
        pg.K_w: 3,
    }, animators, default=env.IDLE)

    return anim_controller