
import pytest
from pydantic import BaseModel

from tests.unit.fixture import clear_TTForge_singleton

from ttforge.core.item import *

NS = "test"

def test_minimal_definition():

    @item(NS)
    class Foo(ItemBase):
        NAME = "Foo"

def test_weight():

    @item(NS)
    class Foo(ItemBase):
        NAME = "Foo"
        WEIGHT = 1.5

    assert Foo.WEIGHT == 1.5
    foo = Foo()
    assert foo.getWeight() == 1.5
    assert pytest.approx(foo.getWeightOunces(), 0.1) == 52.9

def test_weight_ounces():
    @item(NS)
    class Foo(ItemBase):
        NAME = "Foo"
        WEIGHT = "52.9 oz"

    assert Foo.WEIGHT == 1.5
    foo = Foo()
    assert foo.getWeight() == 1.5
    assert pytest.approx(foo.getWeightOunces(), 0.1) == 52.9

def test_unique():

    @item(NS)
    class ItemNotUnique(ItemBase):
        NAME = "Foo"

    assert not ItemNotUnique.isUnique()

    class ItemUnique(ItemBase):
        NAME = "Bar"
        SERIAL_MODEL = BaseModel

    assert ItemUnique.isUnique()
