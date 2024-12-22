
from typing import *

from ttforge.core.registry import RegistryDict
from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase
from ttforge.core.registry import RegistryMain
from ttforge.core.registry.registry_main import RegistryMainEntryType
from ttforge.core.skill import SkillBase

class TTForgeSystemRegistries:
    MAIN = RegistryMain()
    CHARACTERISTICS = RegistryDict(CharacteristicPrimary)
    CHARACTERISTICS_DERIVED = RegistryDict(CharacteristicDerivedBase)
    SKILLS = RegistryDict(SkillBase)

class TTForgeSystem:

    def __init__(self):
        self.registry = TTForgeSystemRegistries()

    def registerCharacteristicPrimary(self, characteristic: Type[CharacteristicPrimary]):
        # TODO raise
        self.registry.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC)
        self.registry.CHARACTERISTICS.register(characteristic.REGISTRY_ID, characteristic)

    def registerCharacteristicDerived(self, characteristic: Type[CharacteristicDerivedBase]):
        # TODO raise
        self.registry.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC)
        self.registry.CHARACTERISTICS_DERIVED.register(characteristic.REGISTRY_ID, characteristic)

    def registerSkill(self, skill: Type[SkillBase]):
        # TODO raise errors
        self.registry.MAIN.register(skill.REGISTRY_ID, skill, RegistryMainEntryType.SKILL)
        self.registry.SKILLS.register(skill.REGISTRY_ID, skill)
