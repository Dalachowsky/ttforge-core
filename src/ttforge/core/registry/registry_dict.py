
from typing import *

from .registry_base import RegistryBase

from ttforge.core.exception import DuplicateEntry

class RegistryDict(RegistryBase):

    def __init__(self, objectType: type):
        super().__init__(objectType=objectType, keyType=str)

    def register(self, entryID: str, object):
        if entryID in self._registry:
            raise DuplicateEntry(entryID)
        self._registry[entryID] = object

    def get(self, regID: str):
        return self._registry[regID]