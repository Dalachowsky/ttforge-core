
from typing import *

from ttforge.core.registry import RegistryDict
from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase
from ttforge.core.skill import SkillBase

class TTForgeSystemRegistries:
    CHARACTERISTICS = RegistryDict(CharacteristicPrimary)
    CHARACTERISTICS_DERIVED = RegistryDict(CharacteristicDerivedBase)
    SKILLS = RegistryDict(SkillBase)

class TTForgeSystem:

    def __init__(self):
        self.registry = TTForgeSystemRegistries()

    def registerCharacteristicPrimary(self, characteristic: Type[CharacteristicPrimary]):
        # TODO raise
        self.registry.CHARACTERISTICS.register(characteristic.REGISTRY_ID, characteristic)

    def registerCharacteristicDerived(self, characteristic: Type[CharacteristicDerivedBase]):
        # TODO raise
        self.registry.CHARACTERISTICS_DERIVED.register(characteristic.REGISTRY_ID, characteristic)

    def registerSkill(self, skill: Type[SkillBase]):
        # TODO raise errors
        self.registry.SKILLS.register(skill.REGISTRY_ID, skill)
