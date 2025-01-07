
import re

from ttforge.core import TTForgeObject, ttforge_object, tag
from ttforge.core.exception import TTForgeException

from ttforge.system import TTForgeSystem

class TTForgeOuncesParsingError(TTForgeException):
    def __init__(self, weightString: str) -> None:
        super().__init__(f"Cannot parse ounces from \"{weightString}\"")

def parseOunces(weightOz: str):
    try:
        return round(float(re.match(r"(\d+\.?\d*)\s*oz", weightOz).group(1)) / 35.27, 2)
    except Exception as e:
        raise TTForgeOuncesParsingError(weightOz) 

class ItemBase(TTForgeObject):

    # Weight in kg
    WEIGHT = 0.0

    def __init__(self):
        pass

    def getWeight(self):
        """Weight in kg"""
        return self.WEIGHT

    def getWeightOunces(self):
        return self.WEIGHT * 35.27

class ItemContainer(ItemBase):

    def __init__(self):
        # TODO inventory class
        self._inventory = []

    def getWeight(self):
        """Weight in kg"""
        return sum([item.getWeight() for item in self._inventory])

    def getWeightOunces(self):
        return sum([item.getWeightOunces() for item in self._inventory])

def tagItemSlot(slotID: str):
    """
    Add tag core:itemSlot to class.
    This is a recommended way to indicate that item is equippable.
    """
    def decorator(cls: type[ItemBase]):
        # TODO check slot ID?
        tag("core:itemSlot", slotID)(cls)
        return cls
    return decorator

def item(namespace: str):
    def decorator(cls: type[ItemBase]):
        ttforge_object(namespace)(cls)

        if isinstance(cls.WEIGHT, str):
            cls.WEIGHT = parseOunces(cls.WEIGHT)
        TTForgeSystem().registry.registerItem(cls)
        return cls
    return decorator
