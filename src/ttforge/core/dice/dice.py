
import random
from abc import ABC, abstractmethod

class IDie(ABC):
    @staticmethod
    @abstractmethod
    def roll() -> float:
        pass

class D2(IDie):
    def roll() -> int:
        return random.randint(1, 2)

class D4(IDie):
    def roll() -> int:
        return random.randint(1, 4)

class D6(IDie):
    def roll() -> int:
        return random.randint(1, 6)

class D8(IDie):
    def roll() -> int:
        return random.randint(1, 8)

class D100(IDie):
    def roll() -> int:
        return random.randint(1, 100)