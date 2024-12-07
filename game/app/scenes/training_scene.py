from app.players.battle_doll import BattleDoll
from app.scenes import GameScene
from app.scenes.spell_panel import create_panel


class TrainingScene(GameScene):
    __key__ = "Training"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()
        doll = BattleDoll((w // 2, h // 2), (80, 80), self._player_group, self._draw_group)

        spells = self._player.spells()

        create_panel(spells, w, self._ui_group)



