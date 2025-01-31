
from abc import ABC, abstractmethod
from typing import *

from ttforge.system import TTForgeSystem
from ttforge.core.entity import TTForgeEntity
from ttforge.core.characteristic import CharacteristicBase
from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase, sortDerivedCharacteristics
from ttforge.core.exception import TTForgeException

class CharacteristicNotPresent(TTForgeException):
    def __init__(self, characterName: str, characteristicName: str):
        super().__init__(f"Character \"{characterName}\" does not have a characteristic {characteristicName}")

class DuplicateCharacteristic(TTForgeException):
    def __init__(self, characteristicID: str) -> None:
        super().__init__(f"Characteristic {characteristicID} already present")

class CharacterEntity(TTForgeEntity):

    def __init__(self):
        self._name = ""
        self._characteristics: Dict[str, CharacteristicPrimary]  = {}
        self._derivedCharacteristics: Dict[str, CharacteristicDerivedBase] = {}
        self._initCharacteristics()

    def _initCharacteristics(self):
        """Initialize characteristic internals. Set by @character decorator"""
        pass

    def getCharacteristic(self, registryID: str) -> CharacteristicBase:
        if registryID in self._characteristics:
            return self._characteristics[registryID]
        elif registryID in self._derivedCharacteristics:
            return self._derivedCharacteristics[registryID]
        else:
            raise CharacteristicNotPresent(self._name, registryID)

    def getCharacteristicValue(self, registryID: str):
        return self.getCharacteristic(registryID).getValue()

    @abstractmethod
    def recalculateCharacteristics(self):
        """Method of recalculating characteristics. Based on """
        pass

def character(system: TTForgeSystem):
    def decorator(cls: type[CharacterBase]):
        def _initCharacteristics(self):
            for ch in system.registry.CHARACTERISTICS.objects():
                ch: type[CharacteristicPrimary]
                if ch.REGISTRY_ID in self._characteristics:
                    raise DuplicateCharacteristic(ch.REGISTRY_ID)
                self._characteristics[ch.REGISTRY_ID] = ch(0)

            for ch in system.registry.CHARACTERISTICS_DERIVED.objects():
                ch: type[CharacteristicDerivedBase]
                if ch.REGISTRY_ID in self._characteristics or ch.REGISTRY_ID in self._derivedCharacteristics:
                    raise DuplicateCharacteristic(ch.REGISTRY_ID)
                characteristic = ch()
                characteristic.connectObservables(self.getCharacteristic)
                self._derivedCharacteristics[ch.REGISTRY_ID] = characteristic
        cls._initCharacteristics = _initCharacteristics

        return cls
    return decorator
