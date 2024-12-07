from app.players.battle_doll import BattleDoll
from app.scenes import GameScene
from app.scenes.spell_panel import SpellIcon, SpellPanel


class TrainingScene(GameScene):
    __key__ = "Training"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()
        doll = BattleDoll((w // 2, h // 2), (80, 80), self._player_group, self._draw_group)

        spells = self._player.spells()

        space = 10
        icon_size = 50

        x, y = space, space

        panel = SpellPanel(((icon_size+space)*len(spells) + space, icon_size+2*space), (w//2, 0),
                           "gray", self._ui_group)
        for spell in spells.values():
            icon = SpellIcon((icon_size, icon_size), (x, y), spell)
            x += icon_size + space
            panel.add_spell(icon)


