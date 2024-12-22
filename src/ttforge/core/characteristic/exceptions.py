
from ttforge.core.exception import TTForgeException

class CharacteristicInvalid(TTForgeException):
    pass

class CharacteristicOutOfBounds(TTForgeException):
    def __init__(self, characteristic: "CharacteristicBase", value: any):
        super().__init__(
            f"Value {value} is out of bounds for {characteristic.REGISTRY_ID} [{characteristic.MINVAL}-{characteristic.MAXVAL}]"
        )
