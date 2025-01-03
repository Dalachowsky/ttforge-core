
from typing import *

from ttforge.core.registry import RegistryDict
from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase
from ttforge.core.item import ItemBase
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

    def registerCharacteristicPrimary(self, characteristic: Type[CharacteristicPrimary]):
        # TODO raise
        self.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC)
        self.CHARACTERISTICS.register(characteristic.REGISTRY_ID, characteristic)

    def registerCharacteristicDerived(self, characteristic: Type[CharacteristicDerivedBase]):
        # TODO raise
        self.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC)
        self.CHARACTERISTICS_DERIVED.register(characteristic.REGISTRY_ID, characteristic)

    def registerSkill(self, skill: Type[SkillBase]):
        # TODO raise errors
        self.MAIN.register(skill.REGISTRY_ID, skill, RegistryMainEntryType.SKILL)
        self.SKILLS.register(skill.REGISTRY_ID, skill)

    def registerResourcePool(self, pool: type[ResourcePoolBase]):
        self.MAIN.register(pool.REGISTRY_ID, pool, RegistryMainEntryType.RESOURCE_POOL)
        self.RESOURCE_POOLS.register(pool.REGISTRY_ID, pool)

    def registerItem(self, itemType: type[ItemBase]):
        self.MAIN.register(itemType.REGISTRY_ID, itemType, RegistryMainEntryType.ITEM)
        self.RESOURCE_POOLS.register(itemType.REGISTRY_ID, itemType)

class Singleton(type):
    instance = None
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance

    def __new__(cls, clsname, bases, attrs):
        @classmethod
        def clear(cls):
            if hasattr(cls, "instance"):
                del cls.instance 
        attrs["clear"] = clear
        return type(clsname, bases, attrs)

    def clear(self):
        pass

class TTForgeSystem(metaclass=Singleton):

    def __init__(self):
        self.registry = TTForgeSystemRegistries()
