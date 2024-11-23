import pygame as pg

from app.base.game_object import GameObject
from app.player_animator import AnimationMapBuilder, AnimatorController


class Player(GameObject):
    def __init__(self, pos: tuple[int, int], size:tuple[int, int], group:pg.sprite.Group, speed:int, anim_controller: AnimatorController):
        super().__init__("Player", pos, size, group)

        self._speed = speed
        self._anim_controller = anim_controller
        self._size = size

    @property
    def image(self):
        return pg.transform.scale(self._anim_controller.image, self._size)

    def _move(self):
        pass

    def _attack(self):
        pass

    def update(self):
        self._anim_controller.tick()
        self._move()
        self._attack()

class KeyboardPlayer(Player):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], group: pg.sprite.Group, speed: int,
                 anim_controller: AnimatorController):
        super().__init__(pos, size, group, speed, anim_controller)

    def _move(self):
        if self._anim_controller.animation_name not in [AnimationMapBuilder.IDLE, AnimationMapBuilder.RUN]:
            return

        pressed = pg.key.get_pressed()
        side = self._anim_controller.side
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

        self._anim_controller.move(side)
        self._anim_controller.replace_animation(anim)
        self.rect.center += direction * self._speed

    def _attack(self):
        pressed = pg.key.get_pressed()
        anim = self._anim_controller.animation_name

        if pressed[pg.K_1]:
            anim = AnimationMapBuilder.ATTACK1
        elif pressed[pg.K_2]:
            anim = AnimationMapBuilder.ATTACK2
        elif pressed[pg.K_3]:
            anim = AnimationMapBuilder.ATTACK3

        self._anim_controller.replace_animation(anim)
