
import os
import sys
import logging
import importlib
from typing import *

from ttforge.core.exception import RegistrationError
from ttforge.core.registry import RegistryDict
from ttforge.core.registry import RegistryMain
from ttforge.core.registry.registry_base import RegistryBase
from ttforge.core.registry.registry_main import RegistryMainEntryType
from ttforge.core.ttforge_object import TTForgeObject

if TYPE_CHECKING:
    from ttforge.core.characteristic import CharacteristicPrimary, CharacteristicDerivedBase
    from ttforge.core.item import ItemBase
    from ttforge.core.resourcepool import ResourcePoolBase
    from ttforge.core.skill import SkillBase

LOG = logging.getLogger(f"{__name__}")

class TTForgeSystemRegistries:

    def __init__(self) -> None:
        self.MAIN = RegistryMain()
        self.CHARACTERISTICS = RegistryDict(type['CharacteristicPrimary'])
        self.CHARACTERISTICS_DERIVED = RegistryDict(type['CharacteristicDerivedBase'])
        self.SKILLS = RegistryDict(type['SkillBase'])
        self.RESOURCE_POOLS = RegistryDict(type['ResourcePoolBase'])
        self.ITEMS = RegistryDict(type['ItemBase'])

    def register(self, registryName: str, obj: type[TTForgeObject]):
        if not hasattr(self, registryName):
            raise RegistrationError(f"\"{registryName}\" is not a valid registry")
        reg = getattr(self, registryName)
        if not isinstance(reg, RegistryBase):
            raise RegistrationError(f"\"{registryName}\" is not a valid registry")
        
        self.MAIN.register(obj.REGISTRY_ID, obj, registryName)
        reg.register(obj.REGISTRY_ID, obj)

    def registerCharacteristicPrimary(self, characteristic: type['CharacteristicPrimary']):
        # TODO raise
        self.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC.name)
        self.CHARACTERISTICS.register(characteristic.REGISTRY_ID, characteristic)

    def registerCharacteristicDerived(self, characteristic: type['CharacteristicDerivedBase']):
        # TODO raise
        self.MAIN.register(characteristic.REGISTRY_ID, characteristic, RegistryMainEntryType.CHARACTERISTIC.name)
        self.CHARACTERISTICS_DERIVED.register(characteristic.REGISTRY_ID, characteristic)

    def registerSkill(self, skill: type['SkillBase']):
        # TODO raise errors
        self.MAIN.register(skill.REGISTRY_ID, skill, RegistryMainEntryType.SKILL.name)
        self.SKILLS.register(skill.REGISTRY_ID, skill)

    def registerResourcePool(self, pool: type['ResourcePoolBase']):
        self.MAIN.register(pool.REGISTRY_ID, pool, RegistryMainEntryType.RESOURCE_POOL.name)
        self.RESOURCE_POOLS.register(pool.REGISTRY_ID, pool)

    def registerItem(self, itemType: type['ItemBase']):
        self.MAIN.register(itemType.REGISTRY_ID, itemType, RegistryMainEntryType.ITEM.name)
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

    def importPackages(self, modulesPath: str):
        sys.path.append(modulesPath)
        for moduleDir in os.listdir(modulesPath):
            self.importPackage(os.path.join(modulesPath, moduleDir))

    def importPackage(self, packagePath: str):
        package = os.path.split(packagePath)[-1]
        if not os.path.exists(os.path.join(packagePath, "manifest.json")):
            LOG.warning(f"Module \"{package}\" does not contain manifest.json")
            return
        
        importOrder = [
            "characteristics",
            "skills",
            "items",
        ]

        for m in importOrder:
            # Import static classes
            try:
                importlib.import_module(f"{package}.{m}")
            except ModuleNotFoundError:
                LOG.warning(f"{package}.{m} not found")

        # Import .json files
        # mDataPath = os.path.join(dataPath, m)
