from app.player_animate import get_animate_controller
from app.players.player import Player


class Magician(Player):
    __abstract__ = True

    def __init__(self, folder, sprite_size:tuple[int, int], pos: tuple[int, int], size: tuple[int, int],
                 *groups, spell_groups=(), **kwargs):
        super().__init__(pos, size, *groups, **kwargs)

        self._spell_groups = spell_groups
        animate_controller = get_animate_controller(sprite_size, folder)
        self.set_animate_controller(animate_controller)
