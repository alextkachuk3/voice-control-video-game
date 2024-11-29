import pygame as pg

from app import consts
from app.player_animate import get_animate_controller
from app.players.player import Player


class BattleDoll(Player):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups):
        super().__init__(pos, size, *groups, hp=100)

        animate_controller = get_animate_controller((64, 64), "Assets/Images/Characters/BattleDoll", side_mapper={
            pg.K_s: 0,
            pg.K_a: 0,
            pg.K_d: 0,
            pg.K_w: 0,
        }, delay_overload={consts.HURT: 3})
        self.set_animate_controller(animate_controller)

        self.set_bounding_size((size[0] / 3, size[1] / 1.5))

    def take_damage(self, damage):
        if damage is None:
            return

        if self._hp == 0:
            self._hp = self._max_hp

        self._hp -= damage
        if self._hp < 0:
            self._hp = 0

        self._animate_controller.replace_animation(consts.HURT)
        # TODO: write damage text near doll
