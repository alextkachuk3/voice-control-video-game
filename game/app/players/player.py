from app.base.animator import AnimatedObject


class Player(AnimatedObject):
    def __init__(self, pos: tuple[int, int], size:tuple[int, int], *groups):
        super().__init__("Player", pos, size, *groups, transparent_color=(1, 0, 0))

        self._animate_controller = None
        self._move_controller = None
        self._attack_controller = None

    @property
    def image(self):
        return self._prepare_image(super().image)


    def _on_action_success(self, state=None, side=None):
        if self._animate_controller is None:
            return

        if side:
            self._animate_controller.move(side)

        if state is None:
            return

        self._animate_controller.replace_animation(state)


    def _move(self):
        if self._move_controller is None:
            return

        if self._animate_controller:
            self._move_controller.set_state(self._animate_controller.animation_name)

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

    def update(self):
        super().update()

        self._move()
        self._attack()
