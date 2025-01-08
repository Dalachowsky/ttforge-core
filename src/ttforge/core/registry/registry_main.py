
from typing import *
from enum import Enum, auto
from dataclasses import dataclass

from ...core import TTForgeObject
from ttforge.core.registry import RegistryDict
from ttforge.core.exception import DuplicateEntry

from .registry_base import RegistryBase 

if TYPE_CHECKING:
    from ttforge.core.characteristic.characteristic_derived import CharacteristicDerivedBase
    from ttforge.core.characteristic.characteristic_primary import CharacteristicPrimary

class RegistryMainEntryType(Enum):
    CHARACTERISTIC = 0
    SKILL = auto()
    RESOURCE_POOL = auto()
    ITEM = auto()

@dataclass
class RegistryMainEntry:
    obj: TTForgeObject
    objType: str

class RegistryMain(RegistryDict):

    def __init__(self):
        super().__init__(objectType=TTForgeObject)

    def register(self, entryID: str, object, entryType: str):
        if entryID in self._registry:
            raise DuplicateEntry(entryID, f"Type of the previous entry:{self.get(entryID).objType}")
        entry = RegistryMainEntry(obj=object, objType=entryType)
        self._registry[entryID] = entry

    def get(self, regID: str) -> RegistryMainEntry:
        return self._registry[regID]
