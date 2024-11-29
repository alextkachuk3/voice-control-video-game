import math
from abc import abstractmethod

import pygame as pg

from app import consts
from app.base.animator import Animator, AnimatedObject
from app.base.game_object import GameObject
from app.consts import WIDTH, HEIGHT
from app.iplayer import IPlayer
from app.utility import limit_coordinates


class Spell(AnimatedObject):
    def __init__(self, attack_type, pos, size, *groups, animator: Animator,
                 owner: GameObject = None, damage=None, pin_to_target=True):
        super().__init__("Spell", pos, size, *groups, animator=animator)

        self._animator = animator
        self._owner = owner
        self._damage = damage
        self._attack_type = attack_type
        self._damaged = False
        self._pin_to_target = pin_to_target

    def update(self, colliding_group):
        super().update()

        if self._damaged:
            return

        for obj in colliding_group:
            if obj == self._owner:
                continue

            if not obj.bounding_rect.colliderect(self.bounding_rect):
                continue

            if self._pin_to_target:
                self.rect.center = obj.rect.center
            self._cast()
            self._damaged = True

            if isinstance(obj, IPlayer) and self._damage:
                obj.take_damage(self._damage)
            elif isinstance(obj, Spell):
                obj._cast()

    def __kill(self):
        self._animator.unsubscribe_from_end(self.__kill, (self._attack_type,))
        self.kill()

    def _cast(self):
        self._animator.subscribe_to_end(self.__kill, (self._attack_type,))
        self._animator.replace_animation(self._attack_type)

    @property
    def image(self):
        return self._prepare_image(super().image)


class MoveSpell(Spell):
    def __init__(self, attack_type, pos, size, *groups, animator: Animator, direction: pg.math.Vector2,
                 speed: int = 0, **kwargs):
        super().__init__(attack_type, pos, size, *groups, animator=animator, **kwargs)

        self._direction = direction
        self._speed = speed

        angle = -math.degrees(math.atan2(direction.y, direction.x))

        self.rotate(angle)

    def _move(self):
        self.rect.center += self._direction * self._speed

    def update(self, colliding_group):
        self._move()
        super().update(colliding_group)

        if self.near_bounds(WIDTH, HEIGHT):
            self._cast()

    def _cast(self):
        super()._cast()
        self._speed = 0


class SpellSpawner:
    def __init__(self, attack_type, size, *groups, damage=None, cooldown=0):
        self._size = size
        self._groups = groups
        self._attack_type = attack_type
        self._damage = damage

        self._cooldown = cooldown
        self._time = 0

    def ready(self):
        return self._time == 0

    def update(self):
        if self._time > 0:
            self._time -= 1


class MoveSpellSpawner(SpellSpawner):
    def __init__(self, attack_type, size, *groups, speed=0, **kwargs):
        super().__init__(attack_type, size, *groups, **kwargs)
        self._speed = speed

    @abstractmethod
    def _get_animator(self):
        pass

    def spawn(self, owner, pos, direction, speed=None):
        if not self.ready():
            return

        if speed is None:
            speed = self._speed

        self._time = self._cooldown

        return MoveSpell(self._attack_type, pos, self._size, *self._groups,
                         animator=self._get_animator(), direction=direction, speed=speed, owner=owner,
                         damage=self._damage)


class TargetSpell(Spell):
    def __init__(self, attack_type, pos, size, *groups, animator: Animator,
                 timeout=0, **kwargs):
        super().__init__(attack_type, pos, size, *groups, animator=animator, pin_to_target=False, **kwargs)

        self._timeout = timeout
        self._time = 0

    def update(self, colliding_group):
        self._animator.tick()

        if not self._animator.active(consts.IDLE):
            return

        self._time += 1
        if self._timeout != 0 and self._time >= self._timeout:
            self._cast()

        super().update(colliding_group)


class TargetSpellSpawner(SpellSpawner):
    def __init__(self, attack_type, size, *groups, radius=None, timeout=0, **kwargs):
        super().__init__(attack_type, size, *groups, **kwargs)
        self._radius = radius
        self._timeout = timeout

    @abstractmethod
    def _get_animator(self):
        pass

    def spawn(self, owner, pos):
        if not self.ready():
            return

        if self._radius is not None:
            pos = limit_coordinates(owner.rect.center, pos, self._radius)

        self._time = self._cooldown

        return TargetSpell(self._attack_type, pos, self._size, *self._groups,
                           animator=self._get_animator(), owner=owner, timeout=self._timeout, damage=self._damage)
