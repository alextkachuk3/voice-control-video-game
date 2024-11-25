import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, size:tuple[int, int], pos:tuple[int, int], *groups:list[pg.sprite.Group],
                 label="", color="black", bg_color="gray", outline="black"):
        super().__init__(*groups)

        self.image = pg.surface.Surface(size)

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.image.fill(bg_color)
        pg.draw.rect(self.image, outline, (0, 0, *size), width=1)

        font = pg.font.SysFont("Arial", 20)
        text = font.render(label, True, color)
        rect = text.get_rect()
        rect.center = (size[0] / 2, size[1] / 2)
        self.image.blit(text, rect)

    def is_clicked(self):
        pos = pg.mouse.get_pos()
        left, _, _ = pg.mouse.get_pressed()
        return left and self.rect.collidepoint(pos)

class ImageButton(Button):
    def __init__(self, size:tuple[int, int], pos:tuple[int, int], *groups:list[pg.sprite.Group],
                 image:pg.surface.Surface = None):
        super().__init__(size, pos, *groups)

        if image:
            self.image = pg.transform.scale(image, size)
            self.image.set_colorkey("white")

class TextField(pg.sprite.Sprite):
    def __init__(self, size: tuple[int, int], pos, *groups: list[pg.sprite.Group],
                 color="black", bg_color="white", outline="black"):
        super().__init__(*groups)

        self.image = pg.surface.Surface(size)
        self.image.fill(bg_color)

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.__color = color
        self.__bg_color = bg_color
        self.__outline = outline
        self.__font = pg.font.SysFont("Arial", 40)

        self.value = ""

    def type(self, event):
        if event.type != pg.KEYDOWN:
            return
        if pg.K_a <= event.key <= pg.K_z or pg.K_0 <= event.key <= pg.K_9:
            self.value += chr(event.key)
        if event.key == pg.K_BACKSPACE:
            self.value = self.value[:-1]

    def update(self):
        self.image.fill(self.__bg_color)

        text = self.__font.render(self.value, True, self.__color)
        rect = text.get_rect()
        rect.centery = self.rect.h / 2
        rect.left = 5
        self.image.blit(text, rect)
        pg.draw.rect(self.image, self.__outline, (0, 0, self.rect.w, self.rect.h), width=2)


