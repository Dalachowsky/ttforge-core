
import pytest

from ttforge.core.exception import DuplicateEntry
from ttforge.core.resourcepool.resource_pool_base import ResourcePoolType
from ttforge.system import TTForgeSystem
from ttforge.core.resourcepool import ResourcePoolBase, resourcePool
from ttforge.core.characteristic import CharacteristicPrimary, characteristicPrimary, CharacteristicDerivedBase, characteristicDerived
from ttforge.core.item import ItemBase, item
from ttforge.core.skill import SkillBase, skill

NS = "test"

@pytest.fixture(autouse=True)
def clear_singleton():
    yield
    TTForgeSystem().clear()

def test_singleton():
    a = TTForgeSystem()
    b = TTForgeSystem()
    assert a == b

def test_register_each_type():
    @characteristicPrimary(NS)
    class MockCharacteristic(CharacteristicPrimary):
        NAME = "Mock"

    @characteristicDerived(NS)
    class MockModifier(CharacteristicDerivedBase):
        NAME = "Mock modifier"
        DEPENDENCIES = ["test:mock"]

        def _recalculate(self):
            return self.getDep("test:mock") / 10

    @skill(NS)
    class MockSkill(SkillBase):
        NAME = "Mocking"

    @resourcePool(NS)
    class HealthPool(ResourcePoolBase):
        NAME = "Health points"

        def __init__(self, value: ResourcePoolType, maxval: ResourcePoolType) -> None:
            super().__init__(value, maxval)

    @item(NS)
    class Sword(ItemBase):
        NAME = "Sword"

    sys = TTForgeSystem()

def test_duplicate_registry_ID_different_type():

    @characteristicPrimary(NS)
    class MockCharacteristic(CharacteristicPrimary):
        NAME = "Mock"

    with pytest.raises(DuplicateEntry):
        @skill(NS)
        class MockSkill(SkillBase):
            NAME = "Mock"
