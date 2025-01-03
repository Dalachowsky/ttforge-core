
from typing import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ttforge.core import TTForgeObject, ttforge_object, ttforgeObjectClassFromJSON

from .exceptions import CharacteristicInvalid

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

dynamicChClassesCount = 0
def characteristicBaseClassFromJSON(namespace: str, d: dict):
    global dynamicChClassesCount
    cls = type(f"CharacteristicClass{dynamicChClassesCount}", (CharacteristicBase, ), {})
    dynamicChClassesCount += 1
    ttforgeObjectClassFromJSON(cls, namespace, d)
    cls.ABBREV = d.get("abbrev", None)
    characteristic_base(namespace)(cls)
    return cls

def generateCharacteristicAbbrev(name: str):
    vowels = "aeiou"
    abbrev = "".join(
        [c for c in name if c.lower() not in vowels and c.isalpha()]
    ).upper()
    return abbrev

def characteristic_base(namespace: str):
    '''Decorator for Characteristic'''
    def decorator(cls: type[CharacteristicBase]):
        ttforge_object(namespace)(cls)
        # Set abbreviated name
        if cls.ABBREV is None:
            cls.ABBREV = generateCharacteristicAbbrev(cls.NAME)
        return cls
    return decorator
