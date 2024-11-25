import pygame as pg

from app.player_animate import get_animate_controller
from app.players.player import Player


class BattleDoll(Player):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups):
        super().__init__(pos, size, *groups)

        animate_controller = get_animate_controller((64, 64), "Assets/Images/Characters/BattleDoll", side_mapper={
            pg.K_s: 0,
            pg.K_a: 0,
            pg.K_d: 0,
            pg.K_w: 0,
        })
        self.set_animate_controller(animate_controller)

        self.set_bounding_size((size[0] / 3, size[1] / 2))