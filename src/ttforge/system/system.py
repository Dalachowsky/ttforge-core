
from typing import *

from ttforge.core.registry import RegistryDict
from ttforge.core.registry import RegistryMain
from ttforge.core.registry.registry_main import RegistryMainEntryType

if TYPE_CHECKING:
    from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase
    from ttforge.core.item import ItemBase
    from ttforge.core.resourcepool import ResourcePoolBase
    from ttforge.core.skill import SkillBase

class TTForgeSystemRegistries:

    def __init__(self) -> None:
        self.MAIN = RegistryMain()
        self.CHARACTERISTICS = RegistryDict(type['CharacteristicPrimary'])
        self.CHARACTERISTICS_DERIVED = RegistryDict(type['CharacteristicDerivedBase'])
        self.SKILLS = RegistryDict(type['SkillBase'])
        self.RESOURCE_POOLS = RegistryDict(type['ResourcePoolBase'])
        self.ITEMS = RegistryDict(type['ItemBase'])

    def registerCharacteristicPrimary(self, characteristic: type['CharacteristicPrimary']):
        # TODO raise
        self.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC)
        self.CHARACTERISTICS.register(characteristic.REGISTRY_ID, characteristic)

    def registerCharacteristicDerived(self, characteristic: type['CharacteristicDerivedBase']):
        # TODO raise
        self.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC)
        self.CHARACTERISTICS_DERIVED.register(characteristic.REGISTRY_ID, characteristic)

    def registerSkill(self, skill: type['SkillBase']):
        # TODO raise errors
        self.MAIN.register(skill.REGISTRY_ID, skill, RegistryMainEntryType.SKILL)
        self.SKILLS.register(skill.REGISTRY_ID, skill)

    def registerResourcePool(self, pool: type['ResourcePoolBase']):
        self.MAIN.register(pool.REGISTRY_ID, pool, RegistryMainEntryType.RESOURCE_POOL)
        self.RESOURCE_POOLS.register(pool.REGISTRY_ID, pool)

    def registerItem(self, itemType: type['ItemBase']):
        self.MAIN.register(itemType.REGISTRY_ID, itemType, RegistryMainEntryType.ITEM)
        self.RESOURCE_POOLS.register(itemType.REGISTRY_ID, itemType)

class Singleton(type):
    instance = None
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls.instance.registry = TTForgeSystemRegistries()
        return cls.instance


class TTForgeSystem:

    __instance = None 

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(TTForgeSystem, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):      
        if self.__initialized: return

        self.clear()
        self.__initialized = True

    def clear(self):
        self.registry = TTForgeSystemRegistries()
