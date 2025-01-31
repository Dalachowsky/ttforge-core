
import pytest
import pytest_mock

from ttforge.system.system import TTForgeSystem

from tests.unit.fixture import clear_TTForge_singleton

from ttforge.core.characteristic.exceptions import CharacteristicOutOfBounds
from ttforge.core.object import TTForgeObjectInvalid
from ttforge.core.characteristic import *
from ttforge.core.dice import D6

NS = "ns"

def test_minimal_definition():

    @characteristicPrimary(NS)
    class Characteristic(CharacteristicPrimary):
        NAME = "Test characteristic"

        def rollCheck(self):
            return 0

    assert Characteristic.ABBREV == "TSTCHRCTRSTC"
    assert Characteristic.ID == "test_characteristic"
    assert Characteristic.REGISTRY_ID == "ns:test_characteristic"
    assert TTForgeSystem().registry.CHARACTERISTICS.get(Characteristic.REGISTRY_ID) == Characteristic

def test_validate_no_name():

    with pytest.raises(TTForgeObjectInvalid):
        @characteristicPrimary(NS)
        class Characteristic(CharacteristicPrimary):

            def rollCheck(self):
                return 0

def test_double_inheritance():

    class Characteristic(CharacteristicPrimary):
        DIE = D6

        def rollCheck(self):
            return self.DIE.roll()
    
    @characteristicPrimary(NS)
    class CharacteristicTest(Characteristic):
        NAME = "Test"

    ch = CharacteristicTest(1)
    ch.rollCheck()

@pytest.mark.parametrize("min, max", [(0, 100), (-100, 100), (0, None)])
def test_bounds_check(min, max):

    @characteristicPrimary(NS)
    class Characteristic(CharacteristicPrimary):
        NAME = "Test characteristic"
        MINVAL = min
        MAXVAL = max

    with pytest.raises(CharacteristicOutOfBounds):
        Characteristic(min - 1)    
    if max is None:
        Characteristic(100)    
    else:
        with pytest.raises(CharacteristicOutOfBounds):
            Characteristic(max + 1)    

def test_fromJSON():

    d = {
        "name": "Mock",
        "abbrev": "MOCK"
    }

    Mock = characteristicBaseClassFromJSON(NS, d)

    assert Mock.NAME == "Mock"
    assert Mock.ID == "mock"
    assert Mock.REGISTRY_ID == "ns:mock"
    assert Mock.ABBREV == "MOCK"
