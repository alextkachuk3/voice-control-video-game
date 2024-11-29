import abc
from abc import abstractmethod


class IPlayer:
    @abstractmethod
    def take_damage(self, damage):
        pass

    @abstractmethod
    def alive(self):
        return True

    @property
    @abc.abstractmethod
    def rect(self):
        pass
