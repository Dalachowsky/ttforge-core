
import pytest

from tests.unit.fixture import clear_TTForge_singleton

from ttforge.core.resourcepool import ResourcePoolBase, resourcePool, IResourcePoolObserver, ResourcePoolUpdateEvent
from ttforge.system.system import TTForgeSystem

NS = "test"

@pytest.fixture()
def RegisterHealthPoints():
    @resourcePool(NS)
    class HP(ResourcePoolBase):
        NAME = "Health points"
        ID = "hp"

        def __init__(self, value: int, maxval: int) -> None:
            super().__init__(value, maxval = maxval)

@pytest.mark.usefixtures("RegisterHealthPoints")
class TestResourcePools:

    def test_minimal_definition(self):
        HP = TTForgeSystem().registry.RESOURCE_POOLS.get("test:hp")

        hp = HP(50, 100)
        assert hp.get() == 50

    def test_bounds_check(self):
        HP = TTForgeSystem().registry.RESOURCE_POOLS.get("test:hp")

        @resourcePool(NS)
        class HP(ResourcePoolBase):
            NAME = "Health points"

            def __init__(self, value: int, maxval: int) -> None:
                super().__init__(value, maxval = maxval)

        hp = HP(50, 100)
        assert hp.get() == 50
        hp.set(110)
        assert hp.get() == 100
        hp.set(-10)
        assert hp.get() == 0

    def test_observer(self):
        HP = TTForgeSystem().registry.RESOURCE_POOLS.get("test:hp")

        class Observer(IResourcePoolObserver):

            def __init__(self) -> None:
                self._eventCaptured = False

            def setExpectedValues(self, old: int, new: int):
                self._expectedOld = old
                self._expectedNew = new

            def onResourcePoolUpdate(self, event: ResourcePoolUpdateEvent):
                assert event.regID == HP.REGISTRY_ID
                assert event.old == self._expectedOld
                assert event.new == self._expectedNew
                self._eventCaptured = True

        hp = HP(50, 100)
        o = Observer()
        hp.registerObserver(o)
        o.setExpectedValues(50, 100)
        hp.set(100)
        o.setExpectedValues(100, 0)
        hp.set(0)
        assert o._eventCaptured

    def test_serialize(self):
        HP = TTForgeSystem().registry.RESOURCE_POOLS.get("test:hp")
        hp = HP(50, 100)

        expected = {
            "id": "test:hp",
            "value": 50,
            "minVal": 0,
            "maxVal": 100,
        }
        assert hp.serialize() == expected

    def test_deserialize(self):
        HP = TTForgeSystem().registry.RESOURCE_POOLS.get("test:hp")

        data = {
            "id": "test:hp",
            "value": 50
        }
        HP.deserialize(data)
