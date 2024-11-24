import pygame as pg

from app import consts
from app.base.animator import AnimatedObject
from app.spell import MoveSpellSpawner, TargetSpellSpawner


class Player(AnimatedObject):
    def __init__(self, pos: tuple[int, int], size:tuple[int, int], *groups,
                 anim_controller, speed=0):
        super().__init__("Player", pos, size, *groups, animator=anim_controller, transparent_color=(1, 0, 0))

        self._speed = speed

    @property
    def image(self):
        return self._prepare_image(super().image)

    def _move(self):
        pass

    def _attack(self):
        pass

    def update(self):
        super().update()
        self._animator.tick()
        self._move()
        self._attack()

SIDE_DIRECTION = {
    pg.K_a: pg.math.Vector2(-1, 0),
    pg.K_w: pg.math.Vector2(0, -1),
    pg.K_s: pg.math.Vector2(0, 1),
    pg.K_d: pg.math.Vector2(1, 0),
}

def get_nearest_side(vector):
    if vector.length() != 0:
        vector = vector.normalize()

    if abs(vector.x) > abs(vector.y):
        if vector.x > 0:
            return pg.K_d
        return pg.K_a

    if vector.y > 0:
        return pg.K_s
    return pg.K_w

class KeyboardPlayer(Player):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups,
                 anim_controller, speed=0):
        super().__init__(pos, size, *groups, anim_controller=anim_controller, speed=speed)
        self.__spells = {}

    def add_spell(self, key, spell_spawner):
        self.__spells[key] = spell_spawner

    def _move(self):
        if self._animator.animation_name not in [consts.IDLE, consts.RUN]:
            return

        pressed = pg.key.get_pressed()
        side = self._animator.side
        direction = pg.math.Vector2(0, 0)
        anim = consts.IDLE

        if pressed[pg.K_a]:
            side = pg.K_a
            anim = consts.RUN
            direction += SIDE_DIRECTION[side]
        elif pressed[pg.K_d]:
            side = pg.K_d
            anim = consts.RUN
            direction += SIDE_DIRECTION[side]

        if pressed[pg.K_w]:
            side = pg.K_w
            anim = consts.RUN
            direction += SIDE_DIRECTION[side]
        elif pressed[pg.K_s]:
            side = pg.K_s
            anim = consts.RUN
            direction += SIDE_DIRECTION[side]

        self._animator.move(side)
        self._animator.replace_animation(anim)
        self.move_by(direction * self._speed)

    def _attack(self):
        if self._animator.animation_name not in [consts.IDLE, consts.RUN]:
            return

        pressed = pg.key.get_pressed()
        anim = self._animator.animation_name

        if pressed[pg.K_1]:
            anim = consts.ATTACK1
        elif pressed[pg.K_2]:
            anim = consts.ATTACK2
        elif pressed[pg.K_3]:
            anim = consts.ATTACK3

        if anim not in self.__spells:
            return

        spell_spawner = self.__spells[anim]
        if isinstance(spell_spawner, MoveSpellSpawner):
            mouse = pg.math.Vector2(pg.mouse.get_pos())
            pos = pg.math.Vector2(self.rect.center)
            delta = mouse - pos
            if delta.length() != 0:
                delta = delta.normalize()
            side = get_nearest_side(delta)
            self._animator.move(side)

            spell_spawner.spawn(self, self.rect.center, delta)
        elif isinstance(spell_spawner, TargetSpellSpawner):
            spell_spawner.spawn(self, pg.mouse.get_pos())

        self._animator.replace_animation(anim)
