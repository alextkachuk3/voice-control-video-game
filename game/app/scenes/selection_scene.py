import pygame as pg

from app.base.scene import SceneController
from app.base.storage import Storage
from app.base.ui import Button
from app.players import Necromancer
from app.players.player_factory import PlayerFactory
from app.scenes.beauty_scene import BeautyScene


class PlayerStatement(pg.sprite.Sprite):
    def __init__(self, topleft, group, player, title, font):
        super().__init__(group)

        self.player = player
        self.player.rect.topleft = (0, 0)

        self.text = font.render(title, False, "black")
        self.text_rect = self.text.get_rect(top=self.player.rect.bottom, centerx=player.rect.w//2)

        w, h, = player.rect.w, player.rect.h + self.text_rect.h
        self.image = pg.surface.Surface((w, h))
        self.image.set_colorkey((1, 0, 0))

        self.rect = self.image.get_rect(topleft=topleft)

        self.is_selected = False

    def _draw(self):
        self.image.fill((1, 0, 0))
        self.image.blit(self.player.image, self.player.rect)
        self.image.blit(self.text, self.text_rect)
        if self.is_selected:
            pg.draw.rect(self.image, "black", (0, 0, self.rect.w, self.rect.h), 2)

    def update(self):
        self.player.update()
        self._draw()

class SelectionPanel(pg.sprite.Sprite):
    def __init__(self, group, center):
        super().__init__(group)

        x = 0
        w, h = 200, 200
        keys = PlayerFactory.keys()

        self.image = pg.surface.Surface(((w+5) * len(keys), h+100))
        self.image.set_colorkey((1, 0, 0))
        self.rect = self.image.get_rect(center=center)

        font = pg.font.Font(None, 40)
        self.statement_group = pg.sprite.Group()
        self.statements = {}

        for key in keys:
            player = PlayerFactory.spawn(key, (0, 0), (w, h))
            st = PlayerStatement((x, 0), self.statement_group, player,
                            key, font)
            self.statements[key] = st

            x += w + 5

    def update(self):
        self.image.fill((1, 0, 0))
        self.statement_group.update()
        self.statement_group.draw(self.image)

        pos = pg.mouse.get_pos()
        left, _, _ = pg.mouse.get_pressed()
        if not left or not self.rect.collidepoint(pos):
            return

        local_mouse_pos = (pos[0] - self.rect.left, pos[1] - self.rect.top)

        for name, st in self.statements.items():
            if st.rect.collidepoint(local_mouse_pos):
                st.is_selected = True
                Storage.set("player", name)
            else:
                st.is_selected = False

class SelectionScene(BeautyScene):
    __title__ = "Selection"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = self.get_size()
        panel = SelectionPanel(self._draw_group, (w//2, h//2))

        self.btn = Button((100, 40), (w//2, 0), self._draw_group,
                                 label="Play", bg_color="green")

        self.btn.rect.top = panel.rect.bottom

    def update(self):
        super().update()
        self._draw_group.update()

        if self.btn.is_clicked():
            SceneController.open_scene(Storage.get("nextscene", "Main"), False, self.get_size())
