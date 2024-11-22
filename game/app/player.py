import pygame as pg

from app.base.game_object import GameObject
from app.player_animator import AnimationMapBuilder, AnimatorController


class Player(GameObject):
    def __init__(self, pos: tuple[int, int], size:tuple[int, int], group:pg.sprite.Group, speed:int, anim_controller: AnimatorController):
        super().__init__("Player", pos, size, group)

        self.__speed = speed
        self.__anim_controller = anim_controller
        self.__size = size

    @property
    def image(self):
        return pg.transform.scale(self.__anim_controller.image, self.__size)

    def _move(self):
        pressed = pg.key.get_pressed()
        side = self.__anim_controller.side
        direction = pg.math.Vector2(0, 0)
        anim = AnimationMapBuilder.IDLE

        if pressed[pg.K_a]:
            side = pg.K_a
            direction += pg.math.Vector2(-1, 0)
            anim = AnimationMapBuilder.RUN
        elif pressed[pg.K_d]:
            side = pg.K_d
            direction += pg.math.Vector2(1, 0)
            anim = AnimationMapBuilder.RUN

        if pressed[pg.K_w]:
            side = pg.K_w
            direction += pg.math.Vector2(0, -1)
            anim = AnimationMapBuilder.RUN
        elif pressed[pg.K_s]:
            side = pg.K_s
            direction += pg.math.Vector2(0, 1)
            anim = AnimationMapBuilder.RUN

        self.__anim_controller.move(side)
        self.__anim_controller.replace_animation(anim)
        self.rect.center += direction * self.__speed

    def update(self):
        self.__anim_controller.tick()
        self._move()
