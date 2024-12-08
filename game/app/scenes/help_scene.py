import pygame as pg

from app.base.scene import SceneController
from app.base.storage import Storage
from app.base.ui import Button
from app.players.player_factory import PlayerFactory
from app.scenes.beauty_scene import BeautyScene
from app.scenes.statement import PlayerStatement
from game.app.base.ui import Label

class HelpScene(BeautyScene):
    __key__ = "Help"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        Label((250, 50), (w // 2, 100), self._draw_group, text="Список команд", bg_color="purple")

        cultist_labels_text = ["Кровава баня", "Земляний спис", "Токсична хмара"]
        necromancer_labels_text = ["Токсична хмара", "Тайфун", "Морозна піка"]
        sorceress_labels_text = ["Стріла полум'я", "Відкладений вибух", "Контактна міна"]

        self.draw_start_position = [190, 240]
        self.draw_hero_ability_list("Cultist", cultist_labels_text)
        self.draw_hero_ability_list("Necromancer",  necromancer_labels_text)
        self.draw_hero_ability_list("Sourceress", sorceress_labels_text)

    def draw_hero_ability_list(self, hero_name: str, hero_abilities: list):
        prev_label = Label((200, 40),  self.draw_start_position, self._draw_group, text=hero_name, bg_color="orange")
        for i, label_text in enumerate(hero_abilities):
            prev_label = Label((200, 40), (self.draw_start_position[0], self.draw_start_position[1] + (i + 1) * 60), self._draw_group, text=label_text, bg_color="paleturquoise")
        self.draw_start_position[0] = self.draw_start_position[0] + 315

    def update(self):
        super().update()
        self._draw_group.update()
