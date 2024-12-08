import random

from app.bot_controllers.bot_controllers import BotMoveController, BotMagicController
from app.players.player_factory import PlayerFactory
from app.players.sorceress import Sorceress
from app.scenes.game_scene import GameScene


class BotScene(GameScene):
    __key__ = "Bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._bot = None
        self.__spawn_bot()

    def __spawn_bot(self):
        w, h = self.get_size()
        keys = PlayerFactory.keys()
        key = random.choice(keys)

        self._bot = PlayerFactory.spawn(key, (w // 4, h // 4), (100, 100), self._player_group, self._draw_group,
                                        spell_groups=(self._spell_group, self._draw_group), hp=100)
        self._bot.set_move_controller(BotMoveController(self._bot, self._player, speed=1))
        self._bot.set_attack_controller(BotMagicController(self._bot, self._player))


    def update(self):
        super().update()
        if self._bot and not self._bot.alive() and self._player and self._player.alive():
            self.__spawn_bot()
            self._player.heal(50)

