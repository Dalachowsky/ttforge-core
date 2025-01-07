
import logging
from typing import *
from abc import ABC, abstractmethod

from ttforge.system import TTForgeSystem

from .characteristic_base import CharacteristicBase, characteristic_base
from .exceptions import CharacteristicInvalid, CharacteristicOutOfBounds

LOG = logging.getLogger(f"{__name__}")

def characteristicPrimary(namespace: str):
    '''Decorator for primary characteristic'''
    def decorator(cls):
        characteristic_base(namespace)(cls)
        if cls.MINVAL is not None or cls.MAXVAL is not None:
            cls.setValue = valueSetterBoundsCheck
        else:
            cls.setValue = valueSetterRaw
        TTForgeSystem().registry.registerCharacteristicPrimary(cls)
        return cls
    return decorator

class CharacteristicPrimary(CharacteristicBase):

    MINVAL: float | int = None
    MAXVAL: float | int = None

    def __init__(self, value) -> None:
        super().__init__(value)
        self.setValue(value)
        self.setBaseValue(value)

    def setValue(self, value: any):
        self._value = value

    def setBaseValue(self, value: any):
        self._baseValue = value

    def getBaseValue(self):
        return self._baseValue

    def rollCheck(self) -> int | float:
        # TODO raise notimplemented
        pass

def valueSetterRaw(self: CharacteristicPrimary, value: any):
    self._value = value
    self._notifyObservers()


def valueSetterBoundsCheck(self: CharacteristicPrimary, value: any):
    if self.MINVAL is not None and value < self.MINVAL:
        raise CharacteristicOutOfBounds(self, value)
    if self.MAXVAL is not None and value > self.MAXVAL:
        raise CharacteristicOutOfBounds(self, value)
    self._value = value
    self._notifyObservers()