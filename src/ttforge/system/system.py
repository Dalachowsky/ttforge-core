
from typing import *

from ttforge.core.registry import RegistryDict
from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase

class TTForgeSystemRegistries:
    CHARACTERISTICS = RegistryDict(CharacteristicPrimary)
    CHARACTERISTICS_DERIVED = RegistryDict(CharacteristicDerivedBase)

class TTForgeSystem:

    def __init__(self):
        self.registry = TTForgeSystemRegistries()

    def registerCharacteristicPrimary(self, characteristic: Type[CharacteristicPrimary]):
        # TODO raise
        self.registry.CHARACTERISTICS.register(characteristic.REGISTRY_ID, characteristic)

    def registerCharacteristicDerived(self, characteristic: Type[CharacteristicDerivedBase]):
        # TODO raise
        self.registry.CHARACTERISTICS_DERIVED.register(characteristic.REGISTRY_ID, characteristic)
