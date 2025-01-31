
import pytest
from pydantic import BaseModel

from tests.unit.fixture import clear_TTForge_singleton

from ttforge.core.inventory import Inventory, InventoryDeserializationError
from ttforge.core.item import ItemBase, item
from ttforge.schema.entity import InventorySchema, InventoryEntryModel
from ttforge.system import TTForgeSystem

NS = "test"

class TestInventory:
    def test_deserialization(self):
        inv = Inventory.deserialize(InventorySchema(content=[]))
        assert inv.getWeight() == 0

    def test_deserialization_example_item(self):

        @item(NS)
        class Gold(ItemBase):
            NAME = "Gold"
            WEIGHT = 0.01


        content = [
            {
                "id": "test:gold"
            }
        ]

        inv = Inventory.deserialize(InventorySchema(content=content))
        assert pytest.approx(inv.getWeight()) == 0.01

    def test_add_to_stack(self):
        @item(NS)
        class Gold(ItemBase):
            NAME = "Gold"
            WEIGHT = 0.01

        content = [
            {
                "id": "test:gold",
                "qty": 100
            }
        ]

        inv = Inventory.deserialize(InventorySchema(content=content))
        assert pytest.approx(inv.getWeight()) == 1

        # Add 100 gold
        inv.add(Gold(), 100)
        assert pytest.approx(inv.getWeight()) == 2


        content_expected = [
            {
                "id": "test:gold",
                "qty": 200
            }
        ]
        assert inv.serialize() == content_expected

    def test_add_unique(self):
        @item(NS)
        class EnchantedSword(ItemBase):
            NAME = "Enchanted sword"
            SERIAL_MODEL = BaseModel

        inv = Inventory()
        inv.add(EnchantedSword())

        swordDict = {
            "id": "test:enchanted_sword",
            "data": {}
        }
        content_expected = [
            swordDict
        ]
        assert inv.serialize() == content_expected

        inv.add(EnchantedSword())
        content_expected = [
            swordDict,
            swordDict
        ]
        assert inv.serialize() == content_expected
