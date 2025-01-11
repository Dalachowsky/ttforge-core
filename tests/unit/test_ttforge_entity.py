
import pytest

from ttforge.core import TTForgeEntity, NoInventory

class TestTTForgeEntity:
    def test_minimal_definition(self):
        e = TTForgeEntity()
        d = e.serialize()
        e2 = TTForgeEntity.deserialize(d)

class TestTTForgeEntityInventory:
    def test_add_inventory(self):
        entity = TTForgeEntity()
        entity.addInventory()
        assert entity.hasInventory()

    def test_serialize_inventory(self):
        entity = TTForgeEntity()
        entity.addInventory()
        d = entity.serialize()
        assert "inventory" in d

    def test_deserialize_inventory(self):
        d = {}
        d["inventory"] = []
        entity = TTForgeEntity.deserialize(d)
        assert entity.hasInventory()

    def test_give_item_no_inventory(self):
        entity = TTForgeEntity()
        with pytest.raises(NoInventory, match="Cannot give item"):
            entity.give("item")

    def test_give_item_with_inventory(self):
        entity = TTForgeEntity()
        entity.addInventory()
        try:
            entity.give("item")
        except NoInventory:
            pytest.fail("NoInventory was raised unexpectedly")
