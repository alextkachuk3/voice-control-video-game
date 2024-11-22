import pygame as pg

from app.base.scene import SceneController


def main():
    pg.init()

    size = (600, 600)
    window = pg.display.set_mode(size)
    pg.display.set_caption("Voice Control Video Game")

    SceneController.open_scene("MainScene", True, size)

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

        pg.display.update()

    pg.quit()

if __name__ == '__main__':
    main()