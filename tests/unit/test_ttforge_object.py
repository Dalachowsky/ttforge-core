
import pytest

from ttforge.core import TTForgeObject, tag, ttforge_object, tagIcon
from ttforge.core.exception import TTForgeException

NS = "test"

def test_tag_object():

    @ttforge_object(NS)
    @tag("foo", "bar")
    class Example(TTForgeObject):
        NAME = "Example"

    assert Example.TAGS["foo"] == "bar"

def test_tag_override():

    @ttforge_object(NS)
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

def test_tag_main_decorator():

    @ttforge_object(NS, tags={
        "foo": "bar"
    })
    class Example(TTForgeObject):
        NAME = "Example"
    
    assert Example.TAGS["foo"] == "bar"

def test_tag_icon():

    @ttforge_object(NS)
    @tagIcon("icon.png")
    class Example(TTForgeObject):
        NAME = "Example"

    assert Example.TAGS["core:icon"] == "icon.png"
