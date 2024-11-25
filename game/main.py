import pygame as pg

from app.base.scene import SceneController
from app.base.storage import Storage
from app.consts import WIDTH, HEIGHT

def main():
    pg.init()

    size = (WIDTH, HEIGHT)
    window = pg.display.set_mode(size)
    pg.display.set_caption("Voice Control Video Game")

    SceneController.open_scene("Main", True, size)
    Storage.set("debug", True)

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

    SceneController.close_all()
    pg.quit()

if __name__ == '__main__':
    main()