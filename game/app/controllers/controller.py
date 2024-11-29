from app.iplayer import IPlayer


class Controller:
    def __init__(self, owner: IPlayer, default_state):
        self._state = default_state
        self._owner = owner
        self._callbacks = []

    def subscribe_on_success(self, callback):
        self._callbacks.append(callback)

    def unsubscribe_on_success(self, callback):
        self._callbacks.remove(callback)

    def _call_all(self, *args, **kwargs):
        if not self._owner.alive():
            return

        for callback in self._callbacks:
            callback(*args, **kwargs)

    def set_state(self, state):
        self._state = state

    def close(self):
        pass
