
from pydantic import BaseModel
from typing import *
from abc import ABC, abstractmethod

from ttforge.core.inventory import Inventory
from ttforge.core.exception import TTForgeException, EntityDeserializationError
from ttforge.schema.entity import TTForgeEntityBaseModel

class NoInventory(TTForgeException):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Entity does not have inventory. {msg}")

class TTForgeEntity(ABC):

    # Pydantic model used for (de)serialization
    SERIAL_MODEL: Optional[type[BaseModel]] = None

    def __init__(self) -> None:
        self._inventory: Optional[Inventory] = None

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

    #########################################
    #
    # Decorators for defining entity classes
    #
    #########################################
