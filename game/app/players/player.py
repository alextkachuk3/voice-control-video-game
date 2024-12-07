import pygame as pg

from app import consts
from app.base.animator import AnimatedObject
from app.iplayer import IPlayer
from app.players.player_factory import PlayerFactory


class Player(AnimatedObject, IPlayer, metaclass=PlayerFactory):
    __abstract__ = True

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], *groups, hp=None):
        super().__init__("Player", pos, size, *groups, transparent_color=(1, 0, 0))

        self._animate_controller = None
        self._move_controller = None
        self._attack_controller = None
        self._max_hp = hp
        self._hp = hp
        self._died = False
        self.__instant_killed = False

    def spells(self):
        if self._attack_controller:
            return self._attack_controller.spells()

        return {}

    def instant_kill(self):
        self._animate_controller.subscribe_to_end(self.__delayed_death, keys=(consts.DEATH, ))
        self._animate_controller.replace_animation(consts.DEATH)

    def __delayed_death(self):
        self._animate_controller.unsubscribe_from_end(self.__delayed_death, keys=(consts.DEATH, ))
        self.close_controllers()
        self.kill()

    @property
    def image(self):
        img = self._prepare_image(super().image)
        if self._max_hp is not None and self._hp > 0:
            h = 10
            pg.draw.rect(img, "gray", (h, 0, self.rect.w - 2 * h, h))
            pg.draw.rect(img, "tomato", (h, 0, int((self.rect.w - 2 * h) * self._hp / self._max_hp), h))
        return img

    def take_damage(self, damage):
        if self._hp is None or damage is None:
            return

        self._hp -= damage
        if self._hp < 0:
            self._hp = 0

        self._died = self._hp <= 0

        self._animate_controller.replace_animation(consts.DEATH if self._died else consts.HURT)

    def _on_action_success(self, state=None, side=None):
        if self._animate_controller is None:
            return

        if side:
            self._animate_controller.move(side)

        if state:
            self._animate_controller.replace_animation(state)

    def _move(self):
        if self._move_controller is None:
            return

        if self._animate_controller:
            self._move_controller.set_state(self._animate_controller.animation_name)
            self._move_controller.set_side(self._animate_controller.side)

        self._move_controller.move()

    def _attack(self):
        if self._attack_controller is None:
            return

        if self._animate_controller:
            self._attack_controller.set_state(self._animate_controller.animation_name)

        self._attack_controller.attack()

    def set_move_controller(self, controller):
        if self._move_controller:
            self._move_controller.unsubscribe_on_success(self._on_action_success)

        self._move_controller = controller

        if controller:
            controller.subscribe_on_success(self._on_action_success)

    def set_attack_controller(self, controller):
        if self._attack_controller:
            self._attack_controller.unsubscribe_on_success(self._on_action_success)

        self._attack_controller = controller

        if controller:
            controller.subscribe_on_success(self._on_action_success)

    def set_animate_controller(self, controller):
        self._animate_controller = controller
        self.set_animator(controller)
        if self._animate_controller:
            self._animate_controller.subscribe_to_end(self.kill, keys=(consts.DEATH,))

    def alive(self):
        return not self._died

    def update(self):
        super().update()

        if self._died:
            return

        self._move()
        self._attack()

        if self.__instant_killed:
            self._hp-=10

        if self._attack_controller:
            self._attack_controller.update()

        rect = self.bounding_rect
        if rect.top < 0:
            rect.top = 0
        elif rect.bottom > consts.HEIGHT:
            rect.bottom = consts.HEIGHT

        if rect.left < 0:
            rect.left = 0
        elif rect.right > consts.WIDTH:
            rect.right = consts.WIDTH

        self.rect.center = rect.center

    def close_controllers(self):
        if self._move_controller:
            self._move_controller.close()

        if self._attack_controller:
            self._attack_controller.close()
