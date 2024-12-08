from app import consts
from app.base.translator import tr
from app.base.ui import Label
from app.scenes.beauty_scene import BeautyScene


class HelpScene(BeautyScene):
    __key__ = "Help"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()

        Label((250, 50), (w // 2, 100), self._draw_group, text=tr("commands"), bg_color="purple")

        cultist_labels_text = tr(consts.BLOOD_BLAST+consts.EARTH_SPIKE+consts.TOXIC_BLAST)
        necromancer_labels_text = tr(consts.FIREBOLT+consts.ICE_SPIKE+consts.WATER_BLAST)
        sorceress_labels_text = tr(consts.FIREBOLT+consts.EXPLOSION+consts.MINE)

        self.draw_start_position = [190, 240]
        self.draw_hero_ability_list(tr("cultist"), cultist_labels_text)
        self.draw_hero_ability_list(tr("necromancer"),  necromancer_labels_text)
        self.draw_hero_ability_list(tr("sorceress"), sorceress_labels_text)

    def draw_hero_ability_list(self, hero_name: str, hero_abilities: list):
        prev_label = Label((200, 40),  self.draw_start_position, self._draw_group, text=hero_name, bg_color="orange")
        for i, label_text in enumerate(hero_abilities):
            prev_label = Label((200, 40), (self.draw_start_position[0], self.draw_start_position[1] + (i + 1) * 60),
                               self._draw_group, text=label_text.title(), bg_color="paleturquoise")
        self.draw_start_position[0] = self.draw_start_position[0] + 315

    def update(self):
        super().update()
        self._draw_group.update()
