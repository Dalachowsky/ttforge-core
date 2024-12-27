
import pytest

from ttforge.core.item import *

NS = "test"

def test_minimal_definition():

    @item(NS)
    @tagItemSlot("core:slot:mainHand")
    class Foo(ItemBase):
        NAME = "Foo"

    assert Foo.TAGS["core:itemSlot"] == "core:slot:mainHand"

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
