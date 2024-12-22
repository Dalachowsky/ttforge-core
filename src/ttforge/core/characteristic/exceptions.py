
from ttforge.core.exception import TTForgeException

class CharacteristicInvalid(TTForgeException):
    pass

class CharacteristicOutOfBounds(TTForgeException):
    def __init__(self, characteristic: "CharacteristicBase", value: any):
        super().__init__(
            f"Value {value} is out of bounds for {characteristic.REGISTRY_ID} [{characteristic.MINVAL}-{characteristic.MAXVAL}]"
        )

class DoesNotDepend(TTForgeException):
    def __init__(self, ch: "CharacteristicDerivedBase", depRegID: str) -> None:
        super().__init__(f"Characteristic {ch.REGISTRY_ID} does not depend on {depRegID}")