from app.players.battle_doll import BattleDoll
from app.scenes import GameScene


class TrainingScene(GameScene):
    __key__ = "Training"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()
        doll = BattleDoll((w // 2, h // 2), (80, 80), self._player_group, self._draw_group)
