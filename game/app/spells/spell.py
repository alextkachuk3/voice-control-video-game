import math
from abc import abstractmethod

import pygame as pg

from app import consts
from app.base.animator import Animator, AnimatedObject
from app.base.game_object import GameObject
from app.consts import WIDTH, HEIGHT
from app.utility import limit_coordinates


class Spell(AnimatedObject):
    def __init__(self, attack_type, pos, size, *groups, animator: Animator, owner: GameObject=None):
        super().__init__("Spell", pos, size, *groups, animator=animator)

        self._animator = animator
        self._owner = owner
        self._attack_type = attack_type

    def update(self, player_group):
        super().update()

        for player in player_group:
            if player == self._owner:
                continue

            if player.bounding_rect.colliderect(self.bounding_rect):
                self.rect.center = player.rect.center
                self._cast()

    def __kill(self):
        self._animator.unsubscribe_from_end(self.__kill, (self._attack_type, ))
        self.kill()

    def _cast(self):
        self._animator.subscribe_to_end(self.__kill, (self._attack_type,))
        self._animator.replace_animation(self._attack_type)


class MoveSpell(Spell):
    def __init__(self, attack_type, pos, size, *groups, animator: Animator, direction: pg.math.Vector2,
                 speed: int = 0, owner: GameObject = None):
        super().__init__(attack_type, pos, size,  *groups, animator=animator, owner=owner)

        self._direction = direction
        self._speed = speed

        angle = -math.degrees(math.atan2(direction.y, direction.x))

        self.rotate(angle)

    @property
    def image(self):
        return self._prepare_image(super().image)

    def _move(self):
        self.rect.center += self._direction * self._speed

    def update(self, player_group):
        self._move()
        super().update(player_group)

        if self.near_bounds(WIDTH, HEIGHT):
            self._cast()

    def _cast(self):
        super()._cast()
        self._speed = 0

class SpellSpawner:
    def __init__(self, attack_type, size, *groups):
        self._size = size
        self._groups = groups
        self._attack_type = attack_type

class MoveSpellSpawner(SpellSpawner):
    def __init__(self, attack_type, size, *groups, speed=0):
        super().__init__(attack_type, size, *groups)
        self._speed = speed

    @abstractmethod
    def _get_animator(self):
        pass

    def spawn(self, owner, pos, direction, speed=None):
        if speed is None:
            speed = self._speed

        return MoveSpell(self._attack_type, pos, self._size,  *self._groups,
                         animator= self._get_animator(), direction=direction, speed=speed, owner=owner)



class TargetSpell(Spell):
    def __init__(self, attack_type, pos, size, *groups, animator: Animator, owner: GameObject = None):
        super().__init__(attack_type, pos, size,  *groups, animator=animator)

    def update(self, collide_group):
        self._animator.tick()
        if not self._animator.active(consts.IDLE):
            return

        for obj in collide_group:
            if obj == self._owner:
                continue

            if obj.bounding_rect.colliderect(self.bounding_rect):
                self._cast()


class TargetSpellSpawner(SpellSpawner):
    def __init__(self, attack_type, size, *groups, radius=None, timeout=0):
        super().__init__(attack_type, size, *groups)
        self._radius = radius
        self._timeout = timeout

    @abstractmethod
    def _get_animator(self):
        pass

    def spawn(self, owner, pos):
        if self._radius is not None:
            pos = limit_coordinates(owner.rect.center, pos, self._radius)

        return TargetSpell(self._attack_type, pos, self._size,   *self._groups,
                           animator=self._get_animator(), owner=owner)
