
import pytest

from ttforge.core.object import TTForgeObject, TTForgeObjectInvalid
from ttforge.core.object.decorator import TTForgeDecoratorBuilder

NS = "test"

def test_required_attribute():

    builder = TTForgeDecoratorBuilder()
    builder.addAttribute("TEST_ATTR", required=True)
    decorator = builder.build()

    with pytest.raises(TTForgeObjectInvalid):
        @decorator(NS)
        class TestClass(TTForgeObject):
            NAME = "test"

    @decorator(NS)
    class TestClass(TTForgeObject):
        NAME = "test"
        TEST_ATTR = "test"

def test_default_attribute():
    builder = TTForgeDecoratorBuilder()
    builder.addAttribute("TEST_ATTR", required=False, default="test")
    decorator = builder.build()

    @decorator(NS)
    class TestClass(TTForgeObject):
        NAME = "test"

    assert TestClass.TEST_ATTR == "test"
