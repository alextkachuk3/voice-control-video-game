from app import consts
from app.players.magician import Magician
from app.spells.firebolt import FireboltSpellSpawner
from app.spells.ice_spike import IceSpikeSpellSpawner
from app.spells.water_blast import WaterBlastSpellSpawner


class Necromancer(Magician):
    __title__ = "Necromancer"

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups, spell_groups=(), **kwargs):
        folder = "Assets/Images/Characters/Necromancer"
        super().__init__(folder, (48, 48), pos, size, *groups, spell_groups=spell_groups, **kwargs)

        self.set_bounding_size((size[0]/3, size[1]/2))

    def set_attack_controller(self, controller):
        super().set_attack_controller(controller)

        if self._attack_controller:
            self._attack_controller.add_spell(consts.ATTACK1, FireboltSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK2, IceSpikeSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK3, WaterBlastSpellSpawner( *self._spell_groups))