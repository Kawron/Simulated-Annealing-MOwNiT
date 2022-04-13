from abc import ABC, abstractmethod


class Node(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getEnergy(self):
        pass

    @abstractmethod
    def neighbour(self, temp):
        pass

    @abstractmethod
    def acceptState(self):
        pass

    @abstractmethod
    def prevState(self):
        pass

    @abstractmethod
    def screenShot(self):
        pass

    @abstractmethod
    def newStartPoint(self):
        pass