
from typing import *

from ttforge.core.registry import RegistryDict
from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase
from ttforge.core.registry import RegistryMain
from ttforge.core.registry.registry_main import RegistryMainEntryType
from ttforge.core.resourcepool import ResourcePoolBase
from ttforge.core.skill import SkillBase

class TTForgeSystemRegistries:

    def __init__(self) -> None:
        self.MAIN = RegistryMain()
        self.CHARACTERISTICS = RegistryDict(CharacteristicPrimary)
        self.CHARACTERISTICS_DERIVED = RegistryDict(CharacteristicDerivedBase)
        self.SKILLS = RegistryDict(SkillBase)
        self.RESOURCE_POOLS = RegistryDict(ResourcePoolBase)
        self.ITEMS = RegistryDict(ItemBase)

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

    def registerResourcePool(self, pool: type[ResourcePoolBase]):
        self.registry.MAIN.register(pool.REGISTRY_ID, pool, RegistryMainEntryType.RESOURCE_POOL)
        self.registry.RESOURCE_POOLS.register(pool.REGISTRY_ID, pool)
