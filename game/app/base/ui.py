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

        self.__color = color
        self.__init_color = color
        self.__enabled = True

        self.bg_color = bg_color
        self.outline = outline
        self.text = text
        self.alignment = alignment

        self.__font = pg.font.SysFont("Arial", font_size)

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value
        self.__color = self.__init_color if value else "gray"

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color
        self.__init_color = color

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
    def __init__(self, size: tuple[int, int], pos: tuple[int, int], *groups: list[pg.sprite.Group], single_click=False,
                 on_clicked=lambda:None,
                 **kwargs):
        super().__init__(size, pos, *groups, **kwargs)

        self.__clicked = False
        self.__delay = 40
        self.__time = 0
        self.__single_click = single_click
        self.__on_clicked = on_clicked

    def update(self):
        super().update()
        if not self.enabled:
            return

        if not self.rect.collidepoint(pg.mouse.get_pos()) and not self.__single_click:
            self.__clicked = False
        self.__time += 1
        if self.__time >= self.__delay and not self.__single_click:
            self.__clicked = False
            self.__time = 0

        self._click()

    def _click(self):
        if self.__clicked:
            return

        pos = pg.mouse.get_pos()
        left, _, _ = pg.mouse.get_pressed()
        self.__clicked = left and self.rect.collidepoint(pos)
        if self.__clicked:
            self.__on_clicked()


class ImageButton(Button):
    def __init__(self, size:tuple[int, int], pos:tuple[int, int], *groups:list[pg.sprite.Group],
                 picture:pg.surface.Surface = None, on_clicked=lambda:None):
        super().__init__(size, pos, *groups, transparent=True, outline="white", bg_color="white",
                         on_clicked=on_clicked)

        if picture:
            self.picture = pg.transform.scale(picture, size)

    def update(self):
        self.image.fill(self.bg_color)
        if self.picture:
            self.image.blit(self.picture, self.picture.get_rect())

        self._click()

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
