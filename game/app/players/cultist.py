from app import consts
from app.players.magician import Magician
from app.spells.blood_blast import BloodBlastSpellSpawner
from app.spells.earth_spike import EarthSpikeSpellSpawner
from app.spells.toxic_blast import ToxicBlastSpellSpawner


class Cultist(Magician):
    __title__ = "cultist"

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups, spell_groups=(), **kwargs):
        folder = "Assets/Images/Characters/Cultist"
        super().__init__(folder, (48, 48), pos, size, *groups, spell_groups=spell_groups, **kwargs)

        self.set_bounding_size((size[0] / 3, size[1] / 2))

    def get_spell_dict(self):
        return {
            consts.ATTACK1: EarthSpikeSpellSpawner(*self._spell_groups),
            consts.ATTACK2: BloodBlastSpellSpawner(*self._spell_groups),
            consts.ATTACK3: ToxicBlastSpellSpawner(*self._spell_groups)
        }