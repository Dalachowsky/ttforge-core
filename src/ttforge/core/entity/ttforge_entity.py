
from pydantic import BaseModel
from typing import *
from abc import ABC, abstractmethod

from ttforge.core.characteristic import CharacteristicBase
from ttforge.core.inventory import Inventory
from ttforge.core.exception import EntryNotFound, TTForgeException, EntityDeserializationError
from ttforge.core.resourcepool import ResourcePoolBase
from ttforge.schema.entity import CharacteristicSchema, TTForgeEntityBaseModel
from ttforge.system import TTForgeSystem

class CharacteristicNotPresent(TTForgeException):
    def __init__(self, characteristicName: str):
        super().__init__(f"Entity does not have a characteristic {characteristicName}")

class NoCharacteristics(TTForgeException):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Entity does not have characteristics. {msg}")

class NoInventory(TTForgeException):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Entity does not have inventory. {msg}")

class NoResourcePool(TTForgeException):
    def __init__(self, resourcePoolID: str) -> None:
        super().__init__(f"Entity does not have resource pool {resourcePoolID}")

class TTForgeEntity(ABC):

    # Pydantic model used for (de)serialization
    SERIAL_MODEL: Optional[type[BaseModel]] = None

    def __init__(self) -> None:
        self._characteristics: Optional[Dict[str, CharacteristicBase]] = None
        self._inventory: Optional[Inventory] = None
        self._resourcePools: Dict[str, ResourcePoolBase] = {}

    @classmethod
    def deserialize(cls, d: dict):
        obj = cls()

        if cls.SERIAL_MODEL is None:
            return obj

        cls.SERIAL_MODEL(json_obj=d)

        if "inventory" in d:
            inventory = d["inventory"]
            obj.deserializeInventory(d["inventory"])
        return obj

    def serialize(self) -> dict:
        d = {}
        if self._inventory is not None:
            d["inventory"] = self._inventory.serialize()
        return d

    # ---------------
    # Characteristics
    # ---------------

    def deserializeCharacteristics(self, characteristics: List[dict]):
        self._characteristics = {}
        for d in characteristics:
            ch_d = CharacteristicSchema.model_validate(d)
            try:
                cls = TTForgeSystem().registry.CHARACTERISTICS.get(ch_d.id)
            except EntryNotFound:
                cls = TTForgeSystem().registry.CHARACTERISTICS_DERIVED.get(ch_d.id)

            self._characteristics[ch_d.id] = cls.deserialize(ch_d.value)

    def hasCharacteristics(self):
        return self._characteristics is not None

    def getCharacteristic(self, id: str):
        if self._characteristics is None:
            raise NoCharacteristics(f"Cannot get {id}")
        ret = self._characteristics.get(id, None)
        if ret is None:
            raise CharacteristicNotPresent(id)
        return ret

    # ---------
    # Inventory
    # ---------

    def deserializeInventory(self, content: dict = {}):
        self._inventory = Inventory.deserialize(content)

    def hasInventory(self):
        return self._inventory is not None

    def give(self, item):
        if not self.hasInventory():
            raise NoInventory(f"Cannot give item")

    # --------------
    # Resource pools
    # --------------

    def deserializeResourcePools(self, pools: List[dict]):
        for entry in pools:
            poolID = entry["id"]
            if self.hasResourcePool(poolID):
                raise EntityDeserializationError(f"Resource pool {poolID} already defined")
            poolType = TTForgeSystem().registry.RESOURCE_POOLS.get(poolID)
            self._resourcePools[poolID] = poolType.deserialize(entry)

    def hasResourcePool(self, resourcePoolID: str):
        return resourcePoolID in self._resourcePools

    def getResourcePool(self, resourcePoolID: str):
        if not self.hasResourcePool(resourcePoolID):
            raise NoResourcePool(resourcePoolID)
        return self._resourcePools[resourcePoolID]

    #########################################
    #
    # Decorators for defining entity classes
    #
    #########################################
