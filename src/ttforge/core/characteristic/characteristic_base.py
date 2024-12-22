
from typing import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ttforge.core import TTForgeObject, ttforge_object

from .exceptions import CharacteristicInvalid

from ttforge.core.registry import validateRegistryID, TTForgeValidateRegistryIDError

@dataclass
class CharacteristicUpdateEvent:
    regID: str
    value: Any

class ICharacteristicObserver(ABC):

    @abstractmethod
    def onCharacteristicUpdate(self, event: CharacteristicUpdateEvent):
        pass

class CharacteristicBase(TTForgeObject, ABC):

    NAME: str = None
    ABBREV: str = None
    ID: str = None
    REGISTRY_ID: str = None

    def __init__(self, value) -> None:
        self._value = value
        self._observers: List[ICharacteristicObserver] = []

    def getValue(self):
        return self._value

    def registerObserver(self, observer: ICharacteristicObserver):
        self._observers.append(observer)

    def _notifyObservers(self):
        event = CharacteristicUpdateEvent(self.REGISTRY_ID, self._value)
        for observer in self._observers:
            observer.onCharacteristicUpdate(event)

def characteristic_base(namespace: str):
    '''Decorator for Characteristic'''
    def decorator(cls: type[CharacteristicBase]):
        ttforge_object(namespace)(cls)
        # Set abbreviated name
        if cls.ABBREV is None:
            vowels = "aeiou"
            abbrev = "".join(
                [c for c in cls.NAME if c.lower() not in vowels and c.isalpha()]
            ).upper()
            cls.ABBREV = abbrev
        return cls
    return decorator
