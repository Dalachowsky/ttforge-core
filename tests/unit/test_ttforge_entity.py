
import pytest
from typing import *
from pydantic import BaseModel

from .fixture import clear_TTForge_singleton

from ttforge.core import entity
from ttforge.core.characteristic import CharacteristicPrimary
from ttforge.core.exception import EntryNotFound
from ttforge.core.entity import TTForgeEntity, NoInventory
from ttforge.core.resourcepool.resource_pool_base import ResourcePoolBase, resourcePool
from ttforge.schema.entity import InventorySchema

NS = "test"

class TestTTForgeEntity:
    def test_minimal_definition(self):
        e = TTForgeEntity()
        d = e.serialize()
        e2 = TTForgeEntity.deserialize(d)

@pytest.fixture()
def MockCharacteristics():
    @CharacteristicPrimary.numeric_int(NS)
    class Foo(CharacteristicPrimary):
        NAME = "Foo"

@pytest.mark.usefixtures("MockCharacteristics")
class TestTTForgeEntityCharacteristics:

    def test_deserialize_characteristics(self):
        characteristics = [
            {
                "id": "test:foo",
                "value": "10"
            }
        ]

        entity = TTForgeEntity()
        assert not entity.hasCharacteristics()

        entity.deserializeCharacteristics(characteristics)

        assert entity.hasCharacteristics()
        assert entity.getCharacteristic("test:foo").getValue() == 10

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

@pytest.fixture()
def MockResourcePool():
    @resourcePool(NS)
    class MockResourcePool(ResourcePoolBase):
        NAME = "Mock points"

@pytest.mark.usefixtures("MockResourcePool")
class TestTTForgeEntityResourcePool:

    def test_deserialize_resource_pool(self):
        entity = TTForgeEntity()

        pools = [
            {
                "id": "test:mock_points",
                "value": 0
            }
        ]
        entity.deserializeResourcePools(pools)
        assert entity.hasResourcePool("test:mock_points")
        entity.getResourcePool("test:mock_points") # Raises Exception if pool not present

    def test_deserialize_invalid_resource_pool(self):
        entity = TTForgeEntity()

        pools = [
            {
                "id": "test:invalid_pool"
            }
        ]
        with pytest.raises(EntryNotFound):
            entity.deserializeResourcePools(pools)

