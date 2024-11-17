import pygame as pg

class SceneController(type):
    __scenes = {}
    __open_scenes = {}
    is_running = True
    __current_scene = "DefaultScene"

    def __new__(cls, name, bases, attrs):
        constructor = type.__new__(cls, name, bases, attrs)

        if "__abstract__" in attrs and attrs["__abstract__"]:
            return constructor

        if "__title__" not in attrs:
            raise TypeError("__title__ must be defined")


        title = attrs["__title__"]
        SceneController.__scenes[title] = constructor

        return constructor

    @staticmethod
    def open_scene(title, close_prev, *args, **kwargs):
        if close_prev and SceneController.__current_scene in SceneController.__open_scenes:
            del SceneController.__open_scenes[SceneController.__current_scene]
        if title in SceneController.__open_scenes:
            SceneController.__current_scene = title
            return

        if title in SceneController.__scenes:
            scene = SceneController.__scenes[title](*args, **kwargs)
            SceneController.__open_scenes[title] = scene
            SceneController.__current_scene = title
            return

        raise ValueError("There no scene with given title")

    @staticmethod
    def scene():
        return SceneController.__open_scenes[SceneController.__current_scene]

class Scene(pg.surface.Surface, metaclass=SceneController):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clock = pg.time.Clock()
        self._draw_group = pg.sprite.Group()

    def handle_event(self, event):
        if event.type == pg.QUIT:
            SceneController.is_running = False

    def close(self):
        pass

    def draw_background(self):
        pass

    def draw(self):
        self.draw_background()
        self._draw_group.draw(self)

    def update(self):
        pass

