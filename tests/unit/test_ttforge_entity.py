
import pytest
from typing import *
from pydantic import BaseModel

from ttforge.core.entity import TTForgeEntity, NoInventory
from ttforge.schema.entity import InventorySchema

class TestTTForgeEntity:
    def test_minimal_definition(self):
        e = TTForgeEntity()
        d = e.serialize()
        e2 = TTForgeEntity.deserialize(d)

class TestTTForgeEntityInventory:
    def test_add_inventory(self):
        entity = TTForgeEntity()
        entity.deserializeInventory({"content": []})
        assert entity.hasInventory()

    def test_serialize_inventory(self):
        entity = TTForgeEntity()
        entity.deserializeInventory()
        d = entity.serialize()
        assert "inventory" in d

    def test_deserialize_inventory(self):
        d = {}
        d["inventory"] = {"content": []}

        class Model(BaseModel):
            inventory: Optional[InventorySchema] = None


        entity = TTForgeEntity
        entity.SERIAL_MODEL = Model
        e = entity.deserialize(d)
        assert e.hasInventory()

    def test_give_item_no_inventory(self):
        entity = TTForgeEntity()
        with pytest.raises(NoInventory, match="Cannot give item"):
            entity.give("item")

    def test_give_item_with_inventory(self):
        entity = TTForgeEntity()
        entity.deserializeInventory()
        try:
            entity.give("item")
        except NoInventory:
            pytest.fail("NoInventory was raised unexpectedly")
