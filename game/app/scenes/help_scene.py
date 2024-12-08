from app import consts
from app.base.translator import tr
from app.base.ui import Label, Image
from app.controllers.attack import MagicController
from app.players.player_factory import PlayerFactory
from app.scenes.beauty_scene import BeautyScene


class HelpScene(BeautyScene):
    __key__ = "Help"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        Label((250, 50), (w // 2, 100), self._draw_group, text=tr("commands"), bg_color="purple")

        spell_spawners = {}

        keys = PlayerFactory.keys()
        for key in keys:
            instance = PlayerFactory.spawn(key, (0, 0), (0, 0))
            controller = MagicController(instance)
            instance.set_attack_controller(controller)

            spell_spawners[key] = controller.spells()

        self.draw_start_position = [190, 240]
        for key, spawners in spell_spawners.items():
            spells = []
            for _, spawner in spawners.items():
                words = spawner.activate_words
                icon = spawner.icon
                spells.append((" ".join(words), icon))

            self.draw_hero_ability_list(tr(key), spells)


    def draw_hero_ability_list(self, hero_name: str, hero_abilities):
        prev_label = Label((200, 40),  self.draw_start_position, self._draw_group, text=hero_name, bg_color="orange")
        for i, ability in enumerate(hero_abilities):
            label_text, icon = ability

            prev_label = Label((200, 40), (self.draw_start_position[0], self.draw_start_position[1] + (i + 1) * 60),
                               self._draw_group, text=label_text.title(), bg_color="paleturquoise")

            image = Image((40, 40), (0, 0), self._draw_group, image=icon)
            image.rect.midright = (prev_label.rect.left-5, prev_label.rect.centery)

        self.draw_start_position[0] = self.draw_start_position[0] + 315

    def update(self):
        super().update()
        self._draw_group.update()
