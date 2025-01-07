from typing import *
from abc import ABC, abstractmethod

from ttforge.core.exception import TTForgeException
from ttforge.core.ttforge_object import TTForgeObject

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

    def objects(self) -> List[TTForgeObject]:
        return self._registry.values()