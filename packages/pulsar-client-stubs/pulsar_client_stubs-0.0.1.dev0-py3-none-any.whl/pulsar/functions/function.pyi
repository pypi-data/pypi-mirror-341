import abc
from abc import abstractmethod

class Function(metaclass=abc.ABCMeta):
    @abstractmethod
    def process(self, input, context): ...
