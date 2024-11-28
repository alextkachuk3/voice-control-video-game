import pygame as pg

class PlayerStatement(pg.sprite.Sprite):
    def __init__(self, topleft, group, player, title, font):
        super().__init__(group)

        self.player = player
        self.player.rect.topleft = (0, 0)

        self.font = font
        self.title = title
        self.color = "black"
        self.text = font.render(title, False, self.color)
        self.text_rect = self.text.get_rect(top=self.player.rect.bottom, centerx=player.rect.w//2)

        w, h, = max(player.rect.w, self.text_rect.w), player.rect.h + self.text_rect.h
        self.image = pg.surface.Surface((w, h))
        self.image.set_colorkey((1, 0, 0))

        self.rect = self.image.get_rect(topleft=topleft)

        self.is_selected = False

    def _draw(self):
        self.image.fill((1, 0, 0))
        self.text = self.font.render(self.title, False, self.color)

        self.image.blit(self.player.image, self.player.rect)
        self.image.blit(self.text, self.text_rect)
        if self.is_selected:
            pg.draw.rect(self.image, "black", (0, 0, self.rect.w, self.rect.h), 2)

    def update(self):
        self.player.update()
        self._draw()