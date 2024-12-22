from typing import *
from abc import ABC, abstractmethod

from ttforge.core.exception import TTForgeException

class RegistrationError(TTForgeException):
    pass


class RegistryBase(ABC):

    def __init__(self, objectType: type, keyType: type = str):
        self._keyType = keyType
        self._objectType = objectType

        self._registry: Dict[keyType, objectType] = {}

    @abstractmethod
    def register(self, entryID: str, object):
        pass

    def items(self):
        return self._registry.items()

    def keys(self):
        return self._registry.keys()

    def objects(self):
        return self._registry.values()

class RegistryDict(RegistryBase):

    def __init__(self, objectType: type):
        super().__init__(objectType=objectType, keyType=str)

    def register(self, entryID: str, object):
        if entryID in self._registry:
            raise RegistrationError(f"ID: {entryID} already registered")
        self._registry[entryID] = object

    def get(self, regID: str):
        return self._registry[regID]
