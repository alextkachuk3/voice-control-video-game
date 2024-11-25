from app import consts
from app.player_animate import get_animate_controller
from app.players.player import Player
from app.spells.firebolt import FireboltSpellSpawner
from app.spells.ice_spike import IceSpikeSpellSpawner
from app.spells.water_blast import WaterBlastSpellSpawner


class Necromancer(Player):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups, spell_groups=()):
        super().__init__(pos, size, *groups)

        self._spell_groups = spell_groups
        folder = "Assets/Images/Characters/Necromancer"
        animate_controller = get_animate_controller((48, 48), folder)
        self.set_animate_controller(animate_controller)

        self.set_bounding_size((size[0]/3, size[1]/2))

    def set_attack_controller(self, controller):
        super().set_attack_controller(controller)

        if self._attack_controller:
            self._attack_controller.add_spell(consts.ATTACK1, FireboltSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK2, IceSpikeSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK3, WaterBlastSpellSpawner( *self._spell_groups))