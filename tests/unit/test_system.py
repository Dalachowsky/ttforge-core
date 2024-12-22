
import pytest

from ttforge.core.exception import DuplicateEntry
from ttforge.system import TTForgeSystem
from ttforge.core.characteristic import CharacteristicPrimary, characteristicPrimary
from ttforge.core.skill import SkillBase, skill

NS = "test"

def test_duplicate_registry_ID_different_type():

    @characteristicPrimary(NS)
    class MockCharacteristic(CharacteristicPrimary):
        NAME = "Mock"

    @skill(NS)
    class MockSkill(SkillBase):
        NAME = "Mock"

    sys = TTForgeSystem()
    sys.registerCharacteristicPrimary(MockCharacteristic)
    with pytest.raises(DuplicateEntry):
        sys.registerSkill(MockSkill)