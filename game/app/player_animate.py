import os
from typing import Any

import pygame as pg

from app import consts
from app.base.animator import Animation, AnimationMapBuilder
from app.controllers.animate import AnimateController


def get_player_animations(size, delay, textures_folder: str,
                          animation_map: dict[Any, tuple[str, bool]],
                          delay_overload: dict[str, int] = None):
    animations = {}

    for name in consts.ALL:
        if name not in animation_map:
            continue

        anim_name, loop = animation_map[name]
        filename = os.path.join(textures_folder, anim_name)
        image = pg.image.load(filename)
        temp_delay = delay
        if delay_overload is not None and name in delay_overload:
            temp_delay = delay_overload[name]

        animation = Animation(image, (0, 0), size, delay=temp_delay, loop=loop)

        animations[name] = animation

    return animations


DEFAULT_SIDE_MAPPER = {
    pg.K_s: 0,
    pg.K_a: 1,
    pg.K_d: 2,
    pg.K_w: 3,
}


def get_animate_controller(size, folder, delay=8, side_mapper: dict[int, int] = None,
                           delay_overload: dict[str, int] = None):
    builder = AnimationMapBuilder(animation_names=consts.ALL)
    anim_map = builder.build_from_files(folder, not_looped=(consts.ATTACK1, consts.ATTACK2, consts.ATTACK3, consts.HURT,
                                                            consts.DEATH, consts.JUMP))
    animations = get_player_animations(size, delay, folder, anim_map, delay_overload)
    anim_controller = AnimateController(DEFAULT_SIDE_MAPPER if side_mapper is None else side_mapper,
                                        animations, default=consts.IDLE)

    return anim_controller
