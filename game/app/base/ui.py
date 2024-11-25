import pygame as pg

class Widget(pg.sprite.Sprite):
    def __init__(self, size:tuple[int, int], pos:tuple[int, int], *groups:list[pg.sprite.Group],
                 text="", color="black", bg_color="white", outline="black", alignment="center",
                 transparent=False, font_size=20):
        super().__init__(*groups)

        self.image = pg.surface.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.image.fill(bg_color)
        if transparent:
            self.image.set_colorkey(bg_color)

        self.color = color
        self.bg_color = bg_color
        self.outline = outline
        self.text = text
        self.alignment = alignment

        self.__font = pg.font.SysFont("Arial", font_size)

    def update(self):
        self.image.fill(self.bg_color)

        text = self.__font.render(self.text, True, self.color)
        rect = text.get_rect()
        if self.alignment == "center":
            rect.center = self.rect.w//2, self.rect.h // 2
        elif self.alignment == "right":
            rect.midright = self.rect.w - 5, self.rect.h // 2
        elif self.alignment == "left":
            rect.midleft = 5, self.rect.h // 2

        self.image.blit(text, rect)
        pg.draw.rect(self.image, self.outline, (0, 0, self.rect.w, self.rect.h), width=2)

class Button(Widget):
    def __init__(self, size: tuple[int, int], pos: tuple[int, int], *groups: list[pg.sprite.Group], **kwargs):
        super().__init__(size, pos, *groups, **kwargs)

        self.__clicked = False
        self.__delay = 20
        self.__time = 0

    def update(self):
        super().update()
        if not self.rect.collidepoint(pg.mouse.get_pos()):
            self.__clicked = False
        self.__time += 1
        if self.__time >= self.__delay:
            self.__clicked = False
            self.__time = 0

    def is_clicked(self):
        if self.__clicked:
            return

        pos = pg.mouse.get_pos()
        left, _, _ = pg.mouse.get_pressed()
        self.__clicked = left and self.rect.collidepoint(pos)
        return self.__clicked

class ImageButton(Button):
    def __init__(self, size:tuple[int, int], pos:tuple[int, int], *groups:list[pg.sprite.Group],
                 picture:pg.surface.Surface = None):
        super().__init__(size, pos, *groups, transparent=True, outline="white", bg_color="white")

        if picture:
            self.picture = pg.transform.scale(picture, size)

    def update(self):
        self.image.fill(self.bg_color)
        if self.picture:
            self.image.blit(self.picture, self.picture.get_rect())

class Label(Widget):
    def __init__(self, size: tuple[int, int], pos, *groups: list[pg.sprite.Group],
                  alignment="left", **kwargs):
        super().__init__(size, pos,*groups, alignment=alignment, **kwargs)

class TextField(Widget):
    def __init__(self, size: tuple[int, int], pos, *groups: list[pg.sprite.Group], alignment="left", **kwargs):
        super().__init__(size, pos, *groups, alignment=alignment, **kwargs)

    def type(self, event):
        if event.type != pg.KEYDOWN:
            return
        if pg.K_a <= event.key <= pg.K_z or pg.K_0 <= event.key <= pg.K_9:
            self.text += chr(event.key)
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
