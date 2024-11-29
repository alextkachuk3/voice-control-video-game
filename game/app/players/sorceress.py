from app import consts
from app.players.magician import Magician
from app.spells.explosion import ExplosionSpellSpawner
from app.spells.firebolt import FireboltSpellSpawner
from app.spells.mine import MineSpellSpawner


class Sorceress(Magician):
    __title__ = "Sorceress"

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups, spell_groups=(), **kwargs):
        folder = "Assets/Images/Characters/Sorceress"
        super().__init__(folder, (48, 48), pos, size, *groups, spell_groups=spell_groups, **kwargs)

        self.set_bounding_size((size[0]/3, size[1]/1.5))

    def set_attack_controller(self, controller):
        super().set_attack_controller(controller)

        if self._attack_controller:
            self._attack_controller.add_spell(consts.ATTACK1, FireboltSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK2, ExplosionSpellSpawner(*self._spell_groups))
            self._attack_controller.add_spell(consts.ATTACK3, MineSpellSpawner(*self._spell_groups))