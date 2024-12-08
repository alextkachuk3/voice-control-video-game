from app.player_animate import get_animate_controller
from app.players.player import Player


class Magician(Player):
    __abstract__ = True

    def __init__(self, folder, sprite_size: tuple[int, int], pos: tuple[int, int], size: tuple[int, int],
                 *groups, spell_groups=(), **kwargs):
        super().__init__(pos, size, *groups, **kwargs)

        self._spell_groups = spell_groups
        animate_controller = get_animate_controller(sprite_size, folder)
        self.set_animate_controller(animate_controller)

    def get_spell_dict(self):
        return {}

    def set_attack_controller(self, controller):
        super().set_attack_controller(controller)

        if self._attack_controller is None:
            return

        spells = self.get_spell_dict()
        for command, spell in spells.items():
            self._attack_controller.add_spell(command, spell)
            self._attack_controller.add_spell(command, spell)
            self._attack_controller.add_spell(command, spell)
