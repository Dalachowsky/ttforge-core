
from .const import NS

from ttforge.core.characteristic import CharacteristicPrimary, characteristicPrimary
from ttforge.core.characteristic import CharacteristicDerivedBase, characteristicDerived


@CharacteristicPrimary.numeric_int(NS)
class Primary(CharacteristicPrimary):
    NAME = "primary"

@characteristicDerived(NS)
class Derived(CharacteristicDerivedBase):
    NAME = "derived"
    DEPENDENCIES = ["test:primary"]
