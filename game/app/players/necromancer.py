from app import consts
from app.players.magician import Magician
from app.spells.firebolt import FireboltSpellSpawner
from app.spells.ice_spike import IceSpikeSpellSpawner
from app.spells.water_blast import WaterBlastSpellSpawner


class Necromancer(Magician):
    __title__ = "necromancer"

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups, spell_groups=(), **kwargs):
        folder = "Assets/Images/Characters/Necromancer"
        super().__init__(folder, (48, 48), pos, size, *groups, spell_groups=spell_groups, **kwargs)

        self.set_bounding_size((size[0] / 3, size[1] / 2))

    def get_spell_dict(self):
        return {
            consts.ATTACK1: FireboltSpellSpawner(*self._spell_groups),
            consts.ATTACK2: IceSpikeSpellSpawner(*self._spell_groups),
            consts.ATTACK3: WaterBlastSpellSpawner(*self._spell_groups)
        }