
import pytest

from tests.unit.fixture import clear_TTForge_singleton

from ttforge.core.skill import SkillBase, skill
from ttforge.core.characteristic import CharacteristicPrimary, characteristicPrimary

NS = "test"

@CharacteristicPrimary.numeric_int(NS)
class CharacteristicMock(CharacteristicPrimary):
    NAME = "Mock"

def test_minimal_definition():

    @skill(NS)
    class SkillTest(SkillBase):
        NAME = "Test skill"
        def _recalculate(self):
            return self._valueBase + 10

    s = SkillTest(10)
    s.recalculate()

    assert s.getValue() == 20

def test_depends_on_characteristic():

    @skill(NS)
    class SkillTest(SkillBase):
        NAME = "Test skill"
        DEPENDENCIES = ["ns:mock"]

        def _recalculate(self):
            return self._valueBase + 10

    mck = CharacteristicMock(10)
    s = SkillTest(10)
    s.connectObservables(lambda k: mck)

    assert s.getValue() == 20
