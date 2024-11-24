import pygame as pg

from app import env
from app.animator_controller import AnimatorController
from app.base.animator import AnimatedObject
from app.spell import MoveSpellSpawner, TargetSpellSpawner


class Player(AnimatedObject):
    def __init__(self, pos: tuple[int, int], size:tuple[int, int], group:pg.sprite.Group, speed:int,
                 anim_controller: AnimatorController):
        super().__init__("Player", pos, size, group, animator=anim_controller)

        self._speed = speed

    @property
    def image(self):
        return self._prepare_image(super().image)

    def _move(self):
        pass

    def _attack(self):
        pass

    def update(self):
        self._animator.tick()
        self._move()
        self._attack()

SIDE_DIRECTION = {
    pg.K_a: pg.math.Vector2(-1, 0),
    pg.K_w: pg.math.Vector2(0, -1),
    pg.K_s: pg.math.Vector2(0, 1),
    pg.K_d: pg.math.Vector2(1, 0),
}

class KeyboardPlayer(Player):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], group: pg.sprite.Group, speed: int,
                 anim_controller: AnimatorController):
        super().__init__(pos, size, group, speed, anim_controller)
        self.__spells = {}

    def add_spell(self, key, spell_spawner):
        self.__spells[key] = spell_spawner

    def _move(self):
        if self._animator.animation_name not in [env.IDLE, env.RUN]:
            return

        pressed = pg.key.get_pressed()
        side = self._animator.side
        direction = pg.math.Vector2(0, 0)
        anim = env.IDLE

        if pressed[pg.K_a]:
            side = pg.K_a
            anim = env.RUN
            direction += SIDE_DIRECTION[side]
        elif pressed[pg.K_d]:
            side = pg.K_d
            anim = env.RUN
            direction += SIDE_DIRECTION[side]

        if pressed[pg.K_w]:
            side = pg.K_w
            anim = env.RUN
            direction += SIDE_DIRECTION[side]
        elif pressed[pg.K_s]:
            side = pg.K_s
            anim = env.RUN
            direction += SIDE_DIRECTION[side]

        self._animator.move(side)
        self._animator.replace_animation(anim)
        self.move_by(direction * self._speed)

    def _attack(self):
        if self._animator.animation_name not in [env.IDLE, env.RUN]:
            return

        pressed = pg.key.get_pressed()
        anim = self._animator.animation_name

        if pressed[pg.K_1]:
            anim = env.ATTACK1
        elif pressed[pg.K_2]:
            anim = env.ATTACK2
        elif pressed[pg.K_3]:
            anim = env.ATTACK3

        if anim not in self.__spells:
            return

        side = self._animator.side
        spell_spawner = self.__spells[anim]
        if isinstance(spell_spawner, MoveSpellSpawner):
            spell_spawner.spawn(self, self.rect.center, SIDE_DIRECTION[side])
        elif isinstance(spell_spawner, TargetSpellSpawner):
            spell_spawner.spawn(self, pg.mouse.get_pos())

        self._animator.replace_animation(anim)
