
import pytest
from typing import *

from tests.unit.fixture import clear_TTForge_singleton

from ttforge.core.characteristic import CharacteristicDerivedBase, characteristicDerived
from ttforge.core.characteristic import characteristicPrimary
from ttforge.core.characteristic import CharacteristicPrimary
from ttforge.core.exception import DoesNotDepend

NS = "ns"

@characteristicPrimary(NS)
class MockCharacteristic(CharacteristicPrimary):
    NAME = "Mock"

def test_minimal_definition():

    @characteristicDerived(NS)
    class CharacteristicDerived(CharacteristicDerivedBase):
        NAME = "Passive wisdom"
        DEPENDENCIES = ["ns:wisdom"]

    assert CharacteristicDerived.NAME == "Passive wisdom"
    
def test_recalculate():

    @characteristicDerived(NS)
    class CharacteristicDerived(CharacteristicDerivedBase):
        NAME = "Derived"
        DEPENDENCIES = ["ns:mock"]

        def _recalculate(self):
            MCK = self.getDep("ns:mock")
            return 10 + MCK

    mock = MockCharacteristic(5)

    ch = CharacteristicDerived()
    assert ch.getValue() == 0
    ch.connectObservables(lambda key: mock)
    assert ch.getValue() == 15
    mock.setValue(20)
    assert ch.getValue() == 30

def test_does_not_depend():

    @characteristicDerived(NS)
    class CharacteristicDerived(CharacteristicDerivedBase):
        NAME = "Derived"
        DEPENDENCIES = ["ns:mock"]

        def _recalculate(self):
            return self.getDep("ns:wisdom")

    ch = CharacteristicDerived()
    with pytest.raises(DoesNotDepend):
        ch.recalculate()

def test_depends_on_derived():

    @characteristicDerived(NS)
    class CharacteristicDerived(CharacteristicDerivedBase):
        NAME = "Derived"
        DEPENDENCIES = ["ns:mock"]

        def _recalculate(self):
            MCK = self.getDep("ns:mock")
            return 10 + MCK

    @characteristicDerived(NS)
    class CharacteristicDerivedSecond(CharacteristicDerivedBase):
        NAME = "Derived second"
        DEPENDENCIES = ["ns:derived"]

        def _recalculate(self):
            VAL = self.getDep("ns:derived")
            return 10 + VAL
        
    characteristics = {
        MockCharacteristic.REGISTRY_ID: MockCharacteristic(10),
        CharacteristicDerived.REGISTRY_ID: CharacteristicDerived(),
        CharacteristicDerivedSecond.REGISTRY_ID: CharacteristicDerivedSecond()
    }

    characteristics[CharacteristicDerived.REGISTRY_ID].connectObservables(lambda key: characteristics[key])
    characteristics[CharacteristicDerivedSecond.REGISTRY_ID].connectObservables(lambda key: characteristics[key])

    assert characteristics[MockCharacteristic.REGISTRY_ID].getValue() == 10
    assert characteristics[CharacteristicDerived.REGISTRY_ID].getValue() == 20
    assert characteristics[CharacteristicDerivedSecond.REGISTRY_ID].getValue() == 30
