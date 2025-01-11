
from typing import *
from abc import ABC, abstractmethod

from ttforge.core.exception import TTForgeException

class EntityDeserializationError(TTForgeException):
    pass

class NoInventory(TTForgeException):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Entity does not have inventory. {msg}")

class TTForgeEntity(ABC):

    def __init__(self) -> None:
        self._inventory = None

    @classmethod
    def deserialize(cls, d: dict):
        obj = cls()
        if "inventory" in d:
            inventory = d["inventory"]
            if not isinstance(inventory, list):
                raise EntityDeserializationError("inventory is not a list")
            obj.addInventory(d["inventory"])
        return obj

    def serialize(self) -> dict:
        d = {}
        if self.hasInventory():
            # TODO inventory class
            d["inventory"] = self._inventory
        return d

    # ---------
    # Inventory
    # ---------

    def addInventory(self, content: List[dict] = []):
        # TODO inventory class
        self._inventory = []

    def hasInventory(self):
        return self._inventory is not None

    def give(self, item):
        # TODO inventory class
        # TODO item type
        if not self.hasInventory():
            raise NoInventory(f"Cannot give item")

    #########################################
    #
    # Decorators for defining entity classes
    #
    #########################################
