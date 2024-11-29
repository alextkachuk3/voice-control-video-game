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

        if "__key__" not in attrs:
            raise TypeError("__title__ must be defined")


        key = attrs["__key__"]
        SceneController.__scenes[key] = constructor

        return constructor

    @staticmethod
    def open_scene(key, close_prev, *args, **kwargs):
        if close_prev and SceneController.__current_scene in SceneController.__open_scenes:
            scene = SceneController.__open_scenes[SceneController.__current_scene]
            scene.close()
            del SceneController.__open_scenes[SceneController.__current_scene]

        pg.mouse.set_visible(True)
        caption = key
        if key in SceneController.__scenes and hasattr(SceneController.__scenes[key], "__caption__"):
            caption = SceneController.__scenes[key].__caption__

        pg.display.set_caption(caption)

        if key in SceneController.__open_scenes:
            SceneController.__current_scene = key
            return

        if key in SceneController.__scenes:
            scene = SceneController.__scenes[key](*args, **kwargs)
            SceneController.__open_scenes[key] = scene
            SceneController.__current_scene = key
            return

        raise ValueError("There no scene with given title")
    @staticmethod
    def close_all():
        for scene in SceneController.__open_scenes.values():
            scene.close()

        SceneController.__open_scenes = {}

    @staticmethod
    def scene():
        return SceneController.__open_scenes[SceneController.__current_scene]

class Scene(pg.surface.Surface, metaclass=SceneController):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clock = pg.time.Clock()
        self._draw_group = pg.sprite.Group()
        self._ui_group = pg.sprite.Group()

    def handle_event(self, event):
        if event.type == pg.QUIT:
            SceneController.is_running = False

    def close(self):
        """
        Calls when scene will be closed
        """
        pass

    def draw_background(self):
        """
        Draws background
        """
        pass

    def draw(self):
        """
        Draws sprites from draw group
        """
        self.draw_background()
        self._draw_group.draw(self)
        self._ui_group.draw(self)

    def update(self):
        self._ui_group.update()

    def tick(self, framerate):
        self._clock.tick(framerate)

