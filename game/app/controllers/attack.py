import pygame as pg

from app import consts
from app.controllers.controller import Controller
from app.spells.spell import MoveSpellSpawner, TargetSpellSpawner
from app.utility import get_nearest_side


class AttackController(Controller):

    def _attack_event(self, state, mouse_pos):
        pass

    def attack(self):
        pass


class MagicController(AttackController):
    def __init__(self, owner, default_state=consts.IDLE):
        super().__init__(owner, default_state)
        self._spells = {}

    def add_spell(self, key, spell_spawner):
        self._spells[key] = spell_spawner

    def _attack_event(self, state, mouse_pos):
        if state not in self._spells or not self._owner.alive():
            return

        spell_spawner = self._spells[state]
        if isinstance(spell_spawner, MoveSpellSpawner):
            mouse = pg.math.Vector2(mouse_pos)
            pos = pg.math.Vector2(self._owner.rect.center)
            delta = mouse - pos
            if delta.length() != 0:
                delta = delta.normalize()
            side = get_nearest_side(delta)

            spell_spawner.spawn(self._owner, self._owner.rect.center, delta)
            self._call_all(state=state, side=side)
            return

        if isinstance(spell_spawner, TargetSpellSpawner):
            spell_spawner.spawn(self._owner, mouse_pos)
            self._call_all(state=state)