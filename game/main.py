import pygame as pg

from app.base.scene import SceneController
from app.base.translator import Translator, tr
from app.consts import WIDTH, HEIGHT
from app.thread_contoller import ThreadController

def main():
    Translator.register_language("Українська", "Assets/Translations/uk.json", encoding="utf-8")
    Translator.register_language("English", "Assets/Translations/en.json")

    pg.init()
    size = (WIDTH, HEIGHT)
    window = pg.display.set_mode(size)
    pg.display.set_caption(tr("Voice Control Video Game"))
    pg.display.set_icon(pg.image.load("Assets/Images/Icon.png"))

    SceneController.open_scene("Main", True, size)

    while SceneController.is_running:
        events = pg.event.get()
        window.fill("black")

        scene = SceneController.scene()

        if scene:
            for event in events:
                scene.handle_event(event)

            scene.update()
            scene.draw()
            window.blit(scene, (0, 0))
            scene.tick(60)

        pg.display.update()
        while not ThreadController.empty():
            func, args, kwargs = ThreadController.get()
            func(*args, **kwargs)

    SceneController.close_all()
    pg.quit()

if __name__ == '__main__':
    main()