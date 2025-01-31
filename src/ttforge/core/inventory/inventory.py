
from typing import *
from dataclasses import dataclass
from pydantic import BaseModel

from ttforge.schema.inventory import InventorySchema, InventoryEntryModel
from ttforge.core.exception import EntityDeserializationError, EntryNotFound
from ttforge.system import TTForgeSystem

if TYPE_CHECKING:
    from ttforge.core.item import ItemBase


class InventoryDeserializationError(EntityDeserializationError):
    def __init__(self, msg = "") -> None:
        super().__init__(f"Cannot deserialize inventory. {msg}")

@dataclass
class InventoryEntry:
    item: "ItemBase"
    quantity: int

class Inventory:

    def __init__(self) -> None:
        self._content: List[InventoryEntry] = []
        self._weight = 0

    @classmethod
    def deserialize(cls, content: dict):
        obj = cls()
        for i, d in enumerate(InventorySchema.model_validate(content).content):
            try:
                itemID = d.id
            except KeyError:
                raise InventoryDeserializationError(f"Item id not found for item {i}")
            
            itemData = d.data            
            quantity = d.qty
            try:
                # Find item by RegID
                itemClass = TTForgeSystem().registry.ITEMS.get(itemID)
                itemClass: ItemBase
                item = itemClass.deserialize(itemData)
                obj.add(item, quantity)
            except KeyError:
                raise InventoryDeserializationError(f"Item id not found for item {i}")
            except Exception as e:
                raise InventoryDeserializationError(f"{e}")
        return obj

    def serialize(self):
        res = []
        for entry in self._content:
            d = InventoryEntryModel(
                id=entry.item.REGISTRY_ID
            )
            if entry.quantity > 1:
                d.qty = entry.quantity
            if entry.item.isUnique():
                d.data = entry.item.serialize()
            res.append(d.model_dump(exclude_unset=True))
        return res

    def _recaulculateWeight(self):
        self._weight = sum([entry.item.getWeight()*entry.quantity for entry in self._content])

    def add(self, item: "ItemBase", quantity = 1):
        if not item.isUnique():
            # Try to add item to stack
            found = None
            for entry in self._content:
                if entry.item.REGISTRY_ID == item.REGISTRY_ID:
                    found = entry
                    break
            if found is not None:
                # Add to stack
                found.quantity += quantity
            else:
                # Stack not found, add new
                self._content.append(InventoryEntry(item, quantity))
        else:
            # Add new unique item
            self._content.append(InventoryEntry(item, quantity))
        self._recaulculateWeight()

    def remove(self, item):
        self._content.remove(item)
        self._recaulculateWeight()

    def getWeight(self):
        return self._weight

    def getWeightOz(self):
        return self._weight * 35.273
