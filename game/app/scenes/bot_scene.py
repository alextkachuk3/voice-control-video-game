from app.scenes.game_scene import GameScene
from app.bot_controllers.bot_controllers import BotMoveController, BotMagicController
from app.players.player_factory import PlayerFactory
from app.player_controllers.keyboard_controllers import KeyboardMoveController
from app.base.storage import Storage
from app.players.sorceress import Sorceress


class BotScene(GameScene):
    __key__ = "Bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = self.get_size()

        self._bot = Sorceress((w // 4, h // 4), (100, 100), self._player_group, self._draw_group,
                              spell_groups=(self._spell_group, self._draw_group), hp=100)
        self._bot.set_move_controller(BotMoveController(self._bot, self._player, speed=1))
        self._bot.set_attack_controller(BotMagicController(self._bot, self._player))

    def update(self):
        super().update()
