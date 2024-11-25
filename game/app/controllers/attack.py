import pygame as pg

from app import consts
from app.controllers.controller import Controller
from app.spells.spell import MoveSpellSpawner, TargetSpellSpawner
from app.utility import get_nearest_side


class AttackController(Controller):

    def _attack_event(self, state):
        pass

    def attack(self):
        pass


class MagicController(AttackController):
    def __init__(self, rect, default_state=consts.IDLE, owner=None):
        super().__init__(rect, default_state, owner=owner)
        self._spells = {}

    def add_spell(self, key, spell_spawner):
        self._spells[key] = spell_spawner

    def _attack_event(self, state):
        if state not in self._spells:
            return

        spell_spawner = self._spells[state]
        if isinstance(spell_spawner, MoveSpellSpawner):
            mouse = pg.math.Vector2(pg.mouse.get_pos())
            pos = pg.math.Vector2(self._rect.center)
            delta = mouse - pos
            if delta.length() != 0:
                delta = delta.normalize()
            side = get_nearest_side(delta)

            spell_spawner.spawn(self._owner, self._rect.center, delta)
            self._call_all(state=state, side=side)
            return

        if isinstance(spell_spawner, TargetSpellSpawner):
            spell_spawner.spawn(self._owner, pg.mouse.get_pos())
            self._call_all(state=state)