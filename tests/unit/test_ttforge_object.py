
import pytest

from ttforge.core.object import TTForgeObject 
from ttforge.core.object.decorator import tag, TTForgeObjectDecorator, tagIcon
from ttforge.core.exception import TTForgeException

NS = "test"

def test_tag_object():

    @TTForgeObjectDecorator(NS)
    @tag("foo", "bar")
    class Example(TTForgeObject):
        NAME = "Example"

    assert Example.TAGS["foo"] == "bar"

def test_tag_override():

    @TTForgeObjectDecorator(NS)
    @tag("foo", "baz")
    @tag("foo", "bar")
    class Example(TTForgeObject):
        NAME = "Example"

    assert Example.TAGS["foo"] == "baz"

def test_tag_untaggable():

    with pytest.raises(TTForgeException):
        @tag("foo", "bar")
        class Example:
            pass

#def test_tag_main_decorator():
#
#    @TTForgeObjectDecorator(NS, tags={
#        "foo": "bar"
#    })
#    class Example(TTForgeObject):
#        NAME = "Example"
#    
#    assert Example.TAGS["foo"] == "bar"

def test_tag_icon():

    @TTForgeObjectDecorator(NS)
    @tagIcon("icon.png")
    class Example(TTForgeObject):
        NAME = "Example"

    assert Example.TAGS["core:icon"] == "icon.png"
