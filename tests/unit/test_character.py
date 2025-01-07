
from tests.unit.fixture import clear_TTForge_singleton

from ttforge.system import TTForgeSystem
from ttforge.core.character import CharacterBase, character
from ttforge.core.characteristic import CharacteristicPrimary, characteristicPrimary, CharacteristicDerivedBase, characteristicDerived

NS = "test"

def test_minimal_definition():

    @characteristicPrimary(NS)
    class Strength(CharacteristicPrimary):
        NAME = "Strength"

    @characteristicDerived(NS)
    class StrengthMod(CharacteristicDerivedBase):
        NAME = "Strength modifier"
        ID = "str_mod"

        DEPENDENCIES = ["test:strength"]

        def _recalculate(self):
            STR = self.getDep("test:strength")
            return 10 + STR

    testSystem = TTForgeSystem()

    @character(testSystem)
    class Character(CharacterBase):

        def recalculateCharacteristics(self):
            pass

    ch = Character()
    assert ch.getCharacteristicValue("test:strength") == 0
    assert ch.getCharacteristicValue("test:str_mod") == 10
