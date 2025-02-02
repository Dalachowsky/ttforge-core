
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
        # Check for deserialize() implementation
        try:
            cls.deserialize("")
        except NotImplementedError as e:
            raise e
        except Exception:
            pass

        # Set valueSetter
        if cls.MINVAL is not None or cls.MAXVAL is not None:
            cls.setValue = valueSetterBoundsCheck
        else:
            cls.setValue = valueSetterRaw

        # Register
        TTForgeSystem().registry.registerCharacteristicPrimary(cls)
        return cls
    return decorator

class CharacteristicPrimary(CharacteristicBase):

    MINVAL: Optional[float | int] = None
    MAXVAL: Optional[float | int] = None

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

    @classmethod
    def deserialize(cls, value: str) -> "CharacteristicPrimary":
        raise NotImplementedError(f"Deserialize method not implemented for characteristic {cls.NAME}")


    # ----------
    # Decorators
    # ----------

    @staticmethod
    def numeric_int(namespace: str, minval: Optional[float | int] = None, maxval: Optional[float | int] = None):
        """Automatically register numeric characteristic"""
        def decorator(cls):
            cls.MINVAL = minval
            cls.MAXVAL = maxval
            @classmethod
            def deserialize_int(cls, value: str):
                obj = cls(int(value))
                return obj
            cls.deserialize = deserialize_int
            characteristicPrimary(namespace)(cls)
            return cls
        return decorator

    @staticmethod
    def numeric_float(namespace: str, minval: Optional[float] = None, maxval: Optional[float] = None):
        """Automatically register numeric characteristic"""
        def decorator(cls):
            cls.MINVAL = minval
            cls.MAXVAL = maxval
            @classmethod
            def deserialize_float(cls, value: str):
                obj = cls(float(value))
                return obj
            cls.deserialize = deserialize_float
            characteristicPrimary(namespace)(cls)
            return cls
        return decorator

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