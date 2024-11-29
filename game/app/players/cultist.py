from app import consts
from app.players.magician import Magician
from app.spells.blood_blast import BloodBlastSpellSpawner
from app.spells.earth_spike import EarthSpikeSpellSpawner
from app.spells.toxic_blast import ToxicBlastSpellSpawner


class Cultist(Magician):
    __title__ = "Cultist"

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups, spell_groups=(), **kwargs):
        folder = "Assets/Images/Characters/Cultist"
        super().__init__(folder, (48, 48), pos, size, *groups, spell_groups=spell_groups, **kwargs)

        self.set_bounding_size((size[0]/3, size[1]/2))

    def set_attack_controller(self, controller):
        super().set_attack_controller(controller)

        if self._attack_controller:
            self._attack_controller.add_spell(consts.ATTACK1, BloodBlastSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK2, EarthSpikeSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK3, ToxicBlastSpellSpawner( *self._spell_groups))